"""dashboard.py

Description:

Primarily this module provides the functionality for the index.html site, as a backend logic system.
The Module utilises Flask to interact with the site, and uses functions to handle requests that are made by the user.


Functions:

    startup()
    index()

    create_schedule(request_args)       # Only called in response to a GET Request from Form containing name="two"
    handle_alarm(request_args)          # Only called in response to a GET Request from Button with name="update-item"
    handle_article(request_args)        # Only called in response to a GET Request from Button with name="notif"

    update_covid(location, location_type)
    update_news(current_articles)

    check_tasks()
    execute_schedule(schedule_object)

    get_user_details(group_name, item_name)

    blacklist_article(article)
    update_schedules_config(schedule_object, remove)

    For further information on what functions do, their parameters, and returns.
    Consult function_name.__doc__ for the docstring
"""

# """
# Sphinx Doc Structure

# --------------------

# :param [paramName]: [paramDescription], defaults to [paramDefaultValue]
# :type [paramName]: [paramType]

# :return: [returnDescription]
# :rtype: [returnType]

# --------------------
# """

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

import time

import sys
import os

import logging
import pytest

import json

import Covid19Dashboard_ah1062.covid_data_handler as cdh
import Covid19Dashboard_ah1062.covid_news_handling as cnh

app = Flask(__name__, template_folder="templates")

#scheduler = sched.scheduler(time.time, time.sleep)    
logging.basicConfig(filename="main.log", filemode="w", format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# app.logger.format = '%(name)s - %(levelname)s - %(message)s'

package_dir = os.path.dirname(os.path.realpath(__file__))

current_schedules = []
current_articles = []

check_covid = True
check_news = True

local_tuple = None
national_tuple = None

@app.route('/')
def startup():
    """Function called when the site is accessed at 127.0.0.1:5000

    :return: Redirect app.route from '/' to '/index' and call index() 
    :rtype: Method Call

    """

    # Overwrites Log File to account for New Session of the Site
    logging.info("New Session Started")
    
    logging.info("Requesting Covid Data, News Articles, and Configurations")

    # Need some sort of threading to prevent halting of site interaction
    
    #check_task = scheduler.enter(60, 1, check_tasks)

    # # Initialises datapoints for presentation on the site
    # # Tuple format ( Tuple(last7days, totalDeaths, hospitalCases), location, locationType )
    # global national_tuple, local_tuple
    # # Fetch new Date, from config.json location, location_type info
    # location = get_user_details("config", "location")
    # location_type = get_user_details("config", "location_type")

    # national_tuple, local_tuple = update_covid(location, location_type)

    # global current_schedules
    # current_schedules = get_user_details("config", "update_intervals")

    # # Individual Article Format ( {"title":title, "content":content} )
    # global current_articles
    # current_articles = cnh.get_news_data()

    # Redirect site to app.route('/index')
    return redirect('/index')

@app.route('/index')
def index():
    """Function called when the site is accessed at 127.0.0.1:5000/index

    :return: render_template of the index.html site file, with embedded data
    :rtype: Method Call

    """
    
    logging.info("Site served to the User")

    global check_covid, check_news
    global national_tuple, local_tuple
    global current_schedules, current_articles

    current_schedules = get_user_details("config", "update_intervals")

    # Execute Function to check for time match for scheduled tasks, site is refreshed to url '/index' every minute as per meta refresh tag 
    check_tasks()

    # If "GET" request made of the '/index' site
    if request.method == "GET":
        # "two" value originates in the Form for Schedule Creation, the only time the value appears
        # Signifies the name of the Scheduled Update, and is required for the Form's completion
        if "two" in request.args:
            create_schedule(request.args)

        # "update_item" originates in the toast interatction with presented scheduled updates on the site
        if "update_item" in request.args:
            handle_alarm(request.args)
                
        # "notif" origintates in the toast interaction with presented news articles on the site
        if "notif" in request.args:
            handle_article(request.args)

    # If Flag for Covid Data Update True
    if check_covid:
        # Fetch new Date, from config.json location, location_type info
        location = get_user_details("config", "location")
        location_type = get_user_details("config", "location_type")

        national_tuple, local_tuple = update_covid(location, location_type)

        # Turn off Flag to prevent updates upon refresh
        check_covid = False

    # If Flag for News Articles Update True
    if check_news:
        current_articles = update_news(current_articles)

        # Turn off Flag to prevent updates upon refresh
        check_news = False

    #scheduler.run(blocking=False)

    # Return a Rendered Template for the Dashboard Site, with Variables formatted by the assigned values in the index() function
    return render_template("index.html", 
        title="Local and National Covid Data",
        updates=current_schedules,
        news_articles=current_articles,
        location=local_tuple[1], 
        nation_location=national_tuple[1],
        local_7day_infections=local_tuple[0][0], 
        national_7day_infections=national_tuple[0][0], 
        hospital_cases="National Hospital Cases: {0}".format(national_tuple[0][2]),
        deaths_total="National Death Total: {1}".format(local_tuple[0][1], national_tuple[0][1])
    )



def create_schedule(request_args):
    """Handle the schedule of an update for the site, via a form.
    Append the created schedule to the global current_schedules array.

    :param request_args: Arguments passed in the html form for schedule creation (request.args)
    :type request_args: Dictionary

    """

    if isinstance(request_args, dict):
        # Create a Dictionary structure to store the properties of the Scheduled Update
        scheduler_info = {
            "two":"",
            "update":"",
            "repeat":"",
            "covid-data":"",
            "news":""
        }

        # Loop through all arguments passed in the GET request ( all values from the Schedule Update Form )
        for i in request_args:
            # All possible arguments are a key in the scheduler_info dictionary structure
            if i in scheduler_info.keys():
                # Assigns the value of each argument to the Key in scheduler_info
                # If No Value for the Current Key, the Pair Value remains an Empty String, and is not utilised
                scheduler_info[i] = request_args.get(i) 

        # Create new Schedule Dictionary Structure with all relevant data for each schedule
        new_schedule = {
            "title":"{0} at {1}".format(scheduler_info["two"], scheduler_info["update"]),
            "content":"Attributes: {0} - {1} - {2}".format(scheduler_info["repeat"], scheduler_info["covid-data"], scheduler_info["news"]),
            "schedule_time":scheduler_info["update"],
            "repeat":scheduler_info["repeat"],
            "covid-data":scheduler_info["covid-data"],
            "news":scheduler_info["news"]
        }

        # Append new schedule to global list, for check every minute to determine execution
        current_schedules.append(new_schedule)
        logging.info(f"Update Scheduled with Name {new_schedule['title']} for Time {new_schedule['schedule_time']}, Attributes: {new_schedule['content']}")
        update_schedules_config(new_schedule, remove=False)

def handle_alarm(request_args):
    """Handle the interaction with an alarm toast on the site.
    Remove the interacted alarm update from the global current_schedules array

    :param request_args: Arguments passed by the Form relating to the toast object (request.args)
    :type request_args: Dictionary

    """

    if isinstance(request_args, dict):
        # Loop through all currently running schedules
        for schedule in current_schedules:
            # If title of schedule identical to interacted schedule 
            if schedule['title'] == request_args.get('update_item'):
                # Remove Interacted Schedule from the List, preventing Execution upon time reach
                current_schedules.remove(schedule)
                update_schedules_config(schedule, remove=True)
                logging.info(f"Scheduled Update with Name {schedule['title']} removed")

                # Break Loop to prevent unnecessary iterations 
                break

def handle_article(request_args):
    """Handle the interaction with an article toast on the site.
    Remove the interacted article from the global current_articles array

    :param request_args: Arguments passed by the Form relating to the toast object (request.args)
    :type request_args: Dictionary

    """

    if isinstance(request_args, dict):
        # Loop through all presented articles, which are stored globally
        for i in current_articles:
            # If title of article identical to interacted article
            if i['title'] == request_args.get('notif'):
                # Remove Interacted Article from the List, preventing display to the user
                current_articles.remove(i)
                logging.info(f"Article removed, URL = {i['title']}")
                
                # Blacklists the Article, meaning it should never be presented to the user again, even upon reload
                blacklist_article(i)
                logging.info(f"Article blacklisted, URL = {i['url']}")
                
                break

        # If List of Currently Displayed Articles is empty, set to fetch new articles upon refresh
        if len(current_articles) == 0:
            check_news = True



def update_covid(location, location_type):
    """Provide a calling point for alarm updates to fetch new covid data

    :param location: Name of the Location to fetch data for
    :type location: String

    :param location_type: The Code given to the Location by the Cov19API
    :type location_type: String

    :return: Fetched national covid data
    :rtype: Tuple

    :return: Fetched local covid data
    :rtype: Tuple

    """

    if isinstance(location, str) and isinstance(location_type, str):
        national_tuple = cdh.get_covid_data(location, location_type)
        local_tuple = cdh.get_covid_data()

        return national_tuple, local_tuple

def update_news(current_articles):
    """Provide a calling point for alarm updates to fetch new articles

    :param current_articles: Global Array of News Articles that are currently presented on the site
    :type current_articles: Array

    :return: Updated article list for presentation
    :rtype: Array

    """

    if isinstance(current_articles, list):
        # Clear Current Articles List and Fetch New List of Articles
        current_articles.clear()
        current_articles = cnh.get_news_data()

        return current_articles



def check_tasks():
    """Perform a check for the execution of scheduled alarm updates

    """

    # Fetch the Current Time in Hours:Minutes Format, to work with Schedule Update Format

    #scheduler.enter(60, 1, check_tasks)

    time_now = "{0}:{1}".format(str(time.localtime(time.time())[3]), str(time.localtime(time.time())[4]))

    # Loop through all currently waiting updates
    for i in current_schedules:
        # If current time identical to scheduled time for update execution
        if time_now == i["schedule_time"]:
            # Execute the Schedule, passing the Structure from current_schedules as a parameter
            execute_schedule(i)

def execute_schedule(schedule_object):
    """Execute the Scheduled Alarm Update, setting flags for data updates in index() for the site
    Remove the alarm update from global array current_schedules if not set to repeat

    :param schedule_object: Dictionary containing the attributes of the scheduled object (name, time, repeat, covid-data, news)
    :type schedule_object: Dictionary

    """

    global check_covid, check_news

    # If "covid-data" is assigned and not an empty string
    if schedule_object["covid-data"] == "covid-data":
        # Flag index() ( app.route('/index') ) for Covid Data Refresh
        check_covid = True

    # If "news" is assigned and not an empty string
    if schedule_object["news"] == "news":
        # Flag index() ( app.route('/index') ) for News Articles Refresh
        check_news = True

    # If "repeat" is not assigned to value "repeat" ( assigned if selected upon schedule creation )
    if schedule_object["repeat"] != "repeat":
        # Remove Schedule from active schedules, to signify it has been executed and won't run again
        current_schedules.remove(schedule_object)
        update_schedules_config(schedule_object, remove=True)



def get_user_details(group_name, item_name):
    """Fetch details/items from the config.json file
    
    :param group_name: Defines which "heading" token to access from (example = "config")
    :type group_name: String

    :param item_name: Defines which token to return the value of (example = "api-key")
    :type item_name: String

    """
    
    # Reads config.json file to access stored details
    with open(package_dir + "\\config.json", "r") as f:
        lines = f.read()
        # Load raw text as json object for navigation, returns specified key, value
        data = json.loads(lines)
        try:
            return data[group_name][item_name]
        except KeyError:
            logging.fatal("KeyError for get_user_details Method Call")
            return None

def blacklist_article(article):
    """Prevent Removed Articles from being presented again by the site.
    Appending the article object to an array in config.json
    
    :param article: Dictionary containing the attributes of the interacted article for blacklist (title, content, url)
    :type article: Dictionary

    """
    
    # Store current list of invalid_articles to present, read from file of articles that have been previously removed
    invalid_articles = []
    with open(package_dir + "\config.json", "r") as f:
        lines = f.read()
        # Load as json for ease of use in adding new blacklisted article
        invalid_articles = json.loads(lines)

    # Append Article to the Json Array of Removed Articles
    invalid_articles["config"]["invalid_articles"].append({"title":article['title'], "content":article['content'], "url":article["url"]})

    # Overwrite invalid_articles.json, with indent for ease of reading and user access
    with open(package_dir + "\config.json", "w") as f:
        json_str = json.dumps(invalid_articles, indent=4)
        f.write(json_str)

def update_schedules_config(schedule_object, remove=False):
    """Store scheduled alarm updates within config.json so that they are valid upon reloading the site.

    :param schedule_object: Dictionary containing the attributes of the scheduled object (name, time, repeat, covid-data, news)
    :type schedule_object: Dictionary

    :param remove: Determine if object is being removed or added to the array, defaults to False
    :type remove: Boolean

    """

    json_str = ""
    
    # Reads config.json file to manage data for manipulation
    with open(package_dir + "\config.json", "r") as f:
        lines = f.read()
        # Loads raw text as json object for navigation
        data = json.loads(lines)

        # Check Flag for Removing or Adding Update Schedules to the config,json array
        if remove == True:
            for i in data["config"]["update_intervals"]:
                if i["title"] == schedule_object["title"]:
                    data["config"]["update_intervals"].remove(i)
                    logging.info(f"Schedule Object with Name {schedule_object['title']} for {schedule_object['schedule_time']} removed from config.json")
                    break
                else:
                    continue
        elif remove == False:
            data["config"]["update_intervals"].append(schedule_object)
            logging.info(f"Schedule Object with Name {schedule_object['title']} for {schedule_object['schedule_time']} saved to config.json")
        else:
            pass

        # Convert the json data back to raw text for overwriting
        json_str = json.dumps(data, indent=4)
    
    # Overwrites previous config.json content with new updated config data
    with open(package_dir + "\config.json", "w") as f:
        f.write(json_str)

def test_functions():
    """Using the pytest module, verify project functionality

    """

    logging.info("Call pytest, test module functionality")
    tests = pytest.main(["-r", sys.path[0]])

    pytest.fixture(fixture_function)

    if tests.OK:
        logging.info(f"Pytest Testing Success: Exit Code Return {tests.OK}")
        return True

    if tests.TESTS_FAILED:
        logging.fatal(f"Fatal Error during pytest: Exit Code Return {tests.TESTS_FAILED}")
        return False
        
        quit()

    # -- Call pytest through cmd

    # os.system(f"cd {sys.path[0]}")
    # os.system("pytest")

def run():
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)