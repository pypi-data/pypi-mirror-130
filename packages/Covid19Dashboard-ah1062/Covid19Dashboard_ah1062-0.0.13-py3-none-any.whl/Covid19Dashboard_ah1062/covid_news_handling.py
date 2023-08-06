"""covid_news_handling.py

Description:

#######

Functions:

    news_API_request(get_user_details, request_terms) # Must be called from the main.py module

    For further information on what functions do, their parameters, and returns.
    Consult function_name.__doc__ for the docstring

"""

import requests
import json

import os

package_dir = os.path.dirname(os.path.realpath(__file__))

# MY API KEY: 41335430eabc4a6ea4818b233d6a92d1 TO STORE

def get_news_data():
    """Call the covid_news_handling module, and fetch new articles in relation to Covid-19

    :return: list of article objects returned by the news_API_request function in covid_news_handling
    :rtype: Array
    """
    
    # Retrieve Articles for presentation
    articles = news_API_request()
    return articles

def news_API_request(request_terms="Covid COVID-19 coronavirus"):
    """Perform a NewsAPI Request and return articles for presentation on the site.

    :param request_terms: Keywords or phrases to be searched for in article titles and bodies, defaults to "Covid COVID-19 coronavirus"
    :type request_terms: String

    :return: Filtered list of article objects, discarding those that have been previously removed
    :rtype: Dictionary
    
    """

    with open(package_dir + "\\config.json", "r") as fc:
        lines = fc.read()
        # Load raw text as json object for navigation, returns specified key, value
        data = json.loads(lines)
        api_key = data["details"]["news-api-key"]

    url = ('https://newsapi.org/v2/everything?q={0}&from=2021-11-13&sortBy=popularity&apiKey={1}'.format(request_terms, api_key))

    response = requests.get(url).content
    response = json.loads(response)["articles"]

    # Generate Set of Articles to not present, read from file of articles that have been previously removed
    invalid_articles = []
    with open(package_dir + "\\config.json", "r") as f:
        lines = f.read()
        stored_invalid = json.loads(lines)

        for i in stored_invalid["config"]["invalid_articles"]:
            invalid_articles.append(i["title"])        
   
   # Generate Set of Articles to present, by comparison of articles retrieved and invalid_articles Set
    valid_articles = []
    for i in response:
        if i['title'] in invalid_articles:
            continue
        else:
            # Take relevant data from the article object retrieved ( that presented on the site )
            article = {"title":i['title'], "content":i['content'], "url":i["url"]}
            valid_articles.append(article)

    return valid_articles