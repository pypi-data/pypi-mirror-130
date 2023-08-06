"""covid_data_handler.py

Description:

#####

Functions:

    parse_csv_data(file_name)
    process_covid_csv_data(covid_csv_data)

    covid_API_request(location, location_type)

    For further information on what functions do, their parameters, and returns.
    Consult function_name.__doc__ for the docstring

"""

from uk_covid19 import Cov19API

import os

package_dir = os.path.dirname(os.path.realpath(__file__))

def parse_csv_data(file_name):
    """Handle a given CSV Filename, to transform the data into a manageable set

    :param csv_filename: The Name of the CSV File, which is placed in the "CSV data files" folder
    :type csv_filename: String

    :return: Parsed CSV File, split into rows of data, and then separated by comma
    :rtype: 2D Array
    """

    if isinstance(file_name, str):
        try:
            # Open File from Folder CSV Data Files
            with open(package_dir + f"\\CSV data files\\{file_name}", "r") as open_csv:
                # Read the Raw Text
                lines = open_csv.readlines()

                for i in range(len(lines)):
                    # Strip all Newline Characters from Row
                    lines[i] = lines[i].strip('\n')
                    # Split Row into an Array by the Comma
                    lines[i] = lines[i].split(",")

            # Return 2D Array of Comma-Split Rows
            return lines
        except FileNotFoundError:
            return None
    else:
        return None

def process_covid_csv_data(covid_csv_data):
    """Process a given CSV File for the required Covid Information to be presented

    :param covid_csv_data: The Return of parse_csv_data, a CSV File split into arrays by line, and then by comma
    :type covid_csv_data: 2D Array

    :return: data_tuple, (last7days_cases, cumulative_deaths, current_hospital_cases)
    :rtype: Tuple

    DOESN'T WORK WITH TEST FILE, FAILS ASSERT FOR LAST 7 DAYS

    """
    
    # Require a return from a valid csv_file, else None
    if covid_csv_data != None:
        last7days_cases, current_hospital_cases, total_deaths = 0, 0, 0
        days_count = 0

        # Take the First Row of Data, which contains the Column Headers for Sorting
        # Detrmine the index of each desired header for use in summing for relevant data
        title_array = covid_csv_data[0]
        index_7days = title_array.index("newCasesBySpecimenDate")
        index_hospital = title_array.index("hospitalCases")
        index_deaths = title_array.index("cumDailyNsoDeathsByDeathDate")

        # Loop through all rows of data until all relevant data is fetched 
        for i in range(1, len(covid_csv_data)):
            if days_count < 7:
                # Skip the First Two Entries because of incomplete data
                if i in range(0,3): 
                    pass
                else:
                    newCases = covid_csv_data[i][index_7days]
                    
                    # Filter Empty Values
                    if newCases != None or "":
                        # Try Except in the case of Invalid Data that can not be cast to an int
                        try:
                            print(f"Index {i} passed")
                            last7days_cases += int(newCases)
                            days_count += 1
                        except ValueError:
                            pass        

            # Only check if variable is "unassigned" to assure most recent data
            if current_hospital_cases == 0:
                hospitalCases = covid_csv_data[i][index_hospital]
                
                if hospitalCases != None or "":
                    # Try Except in the case of Invalid Data that can not be cast to an int
                    try:
                        current_hospital_cases = int(hospitalCases)
                    except ValueError:
                        pass

            # Only check if variable is "unassigned" to assure most recent data
            if total_deaths == 0:
                cumDeaths = covid_csv_data[i][index_deaths]

                if cumDeaths != None or "":
                    # Try Except in the case of Invalid Data that can not be cast to an int
                    try:
                        total_deaths = int(cumDeaths)
                    except ValueError:
                        pass

        # Create tuple for unpacking multiple variables upon return
        data_tuple = (last7days_cases, current_hospital_cases, total_deaths)
        return data_tuple
    else:
        raise Exception("No Covid Data to Process, invalid FileName")

def get_covid_data(location="Exeter", location_type="ltla"):
    """Call the covid_data_handler module, and fetch new covid data for the specified location

    :param location: Name of location to fetch data for, defaults to "Exeter"
    :type location: String

    :param location_type: The Code to identify regionality in the Cov19API, defaults to "ltla"
    :type location_type: String

    :return: data_tuple (tuple of fetched data, location, location_type)
    :rtype: Tuple

    """
    
    if isinstance(location, str) and isinstance(location_type, str):
        # Retrieve Data for presentation
        tuple_values = covid_API_request(location, location_type)
        data_tuple = (tuple_values, location, location_type)

        return data_tuple

def covid_API_request(location="Exeter", location_type="ltla"):
    """Perform a Cov19Api Module API request to fetch Covid Data from the Government statistics

    :param location: Name of location to fetch data for, defaults to "Exeter"
    :type location: String

    :param location_type: The Code to identify regionality in the Cov19API, defaults to "ltla"
    :type location_type: String

    :return: data_tuple, (last7days_cases, cumulative_deaths, current_hospital_cases)
    :rtype: Tuple
    
    """

    # Location Filter Parameters for use in COV19API request
    location_filter = [
        'areaType={0}'.format(location_type),
        'areaName={0}'.format(location)
    ]

    # Structure of Data Metrics to receive from the COV19API request, in Key:Value Format
    data_return_structure = {
        "newCasesBySpecimenDate":"newCasesBySpecimenDate",
        "cumDeaths28DaysByDeathDate":"cumDeaths28DaysByDeathDate",
        "hospitalCases":"hospitalCases"
    }

    # Retrieve Raw Data from the COV19API
    api = Cov19API(filters=location_filter, structure=data_return_structure)
    
    # Convert Raw Data to JSON Format using Cov19API Module
    data = api.get_json()
    
    # Filter Data to the actual dataset, excluding present metadata
    data = data['data']

    last7days_cases, current_hospital_cases, total_deaths = 0, 0, 0
    days_count = 0

    # Loops through all indexes in the Covid Dataset
    # Excludes Index 0 due to incomplete data
    for i in range(1, len(data)):
        # Count limits to taking the previous 7 indexes with a "newCasesBySpecimenDate" Key Value
        if days_count < 6:
            newCases = data[i]['newCasesBySpecimenDate']

            # If there is an assigned value
            if newCases != None or "":
                # Increment the number of days of results that have been collected
                days_count += 1
                # Add the number of cases retrieved to the total for the last 7 days
                last7days_cases += newCases
        else:
            break

        # If there is no value for current_hospital_cases, means only the most recent value will be assigned
        if current_hospital_cases == 0:
            hospital_cases = data[i]['hospitalCases']

            # Do not assign None values, present when using "ltla" as location_type for example
            if hospital_cases != None or "":
                current_hospital_cases = hospital_cases

        # If there is no value for cumulative_deaths, means only the most recent vlaue will be assigned
        if total_deaths ==  0:
            cumulative_deaths = data[i]['cumDeaths28DaysByDeathDate']

            # Do not assign None Values
            if cumulative_deaths != None or "":
                total_deaths = cumulative_deaths

    # Returning an object would be more user-friendly than a tuple
    # Return Tuple of Retrieved Data relevant to the Covid-19 Dashboard Application
    data_tuple = (last7days_cases, total_deaths, current_hospital_cases)
    return data_tuple

if __name__ == "__main__":
    l = "Scotland"
    t = "nation"

    data = covid_API_request(l, t)
    print(data)