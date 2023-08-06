"""
Python module for Tom Sturgeon Computer Science coursework

Functions:
    parse_csv_data(csv_filename: str):
        - Accepts a static file and opens it as a list of strings seperated by a comma
        - Returns the list of strings

    process_covid_csv_data(data: list[str]):
        - Accepts a list of strings and formats it into a list of lists
        - Calculates the current hospital Cases
        - Calculates the total deaths
        - Calculates the new cases in the previous 7 days
        - Returns the 3 calculated values

    covid_API_request(location:str="Exeter", location_type:str="ltla"):
        - Request data from the covid API
        - Stores data acording to the location provided in the function in a json format
        - Stores data from across the nation in a json format

    process_covid_json_data():
        - Calculates the hospital cases from the live data
        - Calculates the total deaths from the live data
        - Calculates the new cases in the last 7 days from the live data
        - Returns the calcualted values

   time_to_update_interval(alarm_time:str):
        - Takes and input of time in the format HH:MM
        - Converts the time into a number of seconds
        - Gets the current time in seconds
        - Works out the number of seconds between the two times
        - Returns the differens of the times

    update_covid_data():
        - Calls covid_API_request() and process_covid_json_data()

    schedule_covid_updates(update_interval:str, update_name:str, repeat:bool = False):
        - Uses the sched module to run update_covid_data
        - Checks weather update interval is a str or not
            - if it is a string converts to a time
            - if not pass the integer to the sched function
        - Retuns a dictionary with the scheduled, name of the update and a description of the update
"""
import json
import sched
import time
import logging
from datetime import datetime as dt
from uk_covid19 import Cov19API
from .shared_functions import time_to_seconds, time_to_update_interval


data_scheduler = sched.scheduler(time.time, time.sleep)

with open('config.json', 'r', encoding="utf8") as config_file:
    config_data = json.load(config_file)

logging.basicConfig(filename=config_data['logging_file'], encoding='utf-8', level=logging.INFO)

local_json_covid_API_data = {}
national_json_covid_API_data = {}
processed_covid_data = {}

def parse_csv_data(csv_filename: str):
    """A function to extract data from a csv document and return a list of strings"""
    with open(csv_filename, "r", encoding="utf8") as csv_file:
        csv_data = csv_file.readlines()
        logging.info("Data Extracted from static file")
    if len(csv_data) < 1:
        logging.warning("No Data Found in Static File")
    return csv_data


def process_covid_csv_data(data: list[str]):
    """
    Processing the data extracted from a static CSV file

    Returns 3 calculated values
        Hospital cases
        Total deaths
        Number of cases in the past 7 days
    """

    # Converts a list of strings into a list of list
    arr = []
    for item in data:
        arr.append(item.split(","))
        arr[len(arr)-1][6] = arr[len(arr)-1][6].strip()

    # Retrives the hospital cases
    hospital_cases = int(arr[1][5])

    # Loops through the array until the total deaths hs been found
    for date in arr:
        if date[4] != "" and date[4] != arr[0][4]:
            total_deaths = int(date[4])
            break

    # Loops through the array from the first completed day of data
    # Adds up the number of cases
    prev_7_days = 0
    for index in range(3, 10):
        prev_7_days += int(arr[index][6])

    logging.info("Data from static file processed")
    return prev_7_days, hospital_cases, total_deaths


def covid_API_request(
    location:str=config_data['search']['location'],
     location_type:str=config_data['search']['location_Type']
     ):
    """
    Request data from the Covid API

    Creats 2 global list of dictionaries one for local data one for national data
    """
    logging.info("Covide data request at " + dt.fromtimestamp(time.time()).strftime('%c'))
    global local_json_covid_API_data
    global national_json_covid_API_data
    local_filter = [
        "areaName="+location,
        "areaType="+location_type
        ]
    national_filter = [
        "areaType=nation",
        "areaName=" + config_data['search']['national_location']
        ]
    local_structure = {
        "date": "date",
        "areaName": "areaName",
        "hospitalCases": "hospitalCases",
        "newCases": "newCasesBySpecimenDate"
    }
    national_structure = {
        "date": "date",
        "areaName": "areaName",
        "deaths": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCases": "newCasesBySpecimenDate"
    }

    local_api = Cov19API(filters=local_filter, structure=local_structure)
    national_api = Cov19API(filters=national_filter, structure=national_structure)
    local_json_covid_API_data = local_api.get_json()
    national_json_covid_API_data = national_api.get_json()
    if len(local_json_covid_API_data) < 1:
        logging.warning("No local Json data returned from the API")
    if len(national_json_covid_API_data) < 1:
        logging.warning("No national Json data returned from the API")
    return local_json_covid_API_data, national_json_covid_API_data


def calc_previous_7_days(covid_data:dict):
    """ From given data it calculates the cases in the previous 7 days """
    total_in_7_days = 0
    index = 0
    while covid_data['data'][index]['newCases'] is None:
        index += 1
    index += 1
    for date in range(index,index+7):
        total_in_7_days += covid_data['data'][date]['newCases']
    logging.debug("7 day total calculated")
    return total_in_7_days

def extract_total_deaths(covid_data:dict):
    """ From the given data it extracts the total number of deaths """
    total_deaths = 0
    index = 0
    while covid_data['data'][index]['deaths'] is None:
        index += 1
    total_deaths = covid_data['data'][index]['deaths']
    logging.debug("Total deaths extracted")
    return total_deaths

def find_hospital_cases(covid_data:dict):
    """ From the given data extract the number of hospital cases """
    index = 0
    while covid_data['data'][index]['hospitalCases'] is None:
        index += 1
    hospital_cases = covid_data['data'][index]['hospitalCases']
    logging.debug("Hospital Cases extracted")
    return hospital_cases


def process_covid_json_data(name:str = "init"):
    """ A function to extract relevent data from a dictionary """
    logging.info("Processing Covid data")
    # extracting the most recent hospital cases
    hospital_cases = find_hospital_cases(national_json_covid_API_data)
    # extracting the previous 7 days cases
    local_prev_7_days = calc_previous_7_days(local_json_covid_API_data)
    nation_prev_7_days = calc_previous_7_days(national_json_covid_API_data)

    # extracting total deaths
    total_deaths = extract_total_deaths(national_json_covid_API_data)
    covid_data = {}
    covid_data['hospitalCases'] = hospital_cases
    covid_data['local7Days'] = local_prev_7_days
    covid_data['nation7Days'] = nation_prev_7_days
    covid_data['totalDeaths'] = total_deaths
    covid_data['remove'] = name


    return covid_data



def update_covid_data(name:str = "init"):
    """ Calls for new covid data request then processes the data """
    logging.info("Covid Data Update Ran at " + dt.fromtimestamp(time.time()).strftime('%c'))
    global processed_covid_data
    covid_API_request()
    processed_covid_data = process_covid_json_data(name)

def covid_data_return():
    """ A function to transfer variable across documents """
    return processed_covid_data

def schedule_covid_updates(update_interval:str, update_name:str, repeat:bool = False):
    """
    A function to schedule covid updates

    Returns a dictionary containing:
    - Title: Update name given by the user
    - Content: what and when the update is for
    - Update: The update Sched object
    - Repeat: Boolean value for weather it repeats or not
    - TimeSec: The time delay in seconds
    - Time: The time of the update to complete
    - Type: Weather its a data update or news
    """
    logging.info("Scheduling a Covid update for " + str(update_interval))
    if isinstance(update_interval,str):
        time_delay = time_to_update_interval(update_interval)
        time_seconds = time_to_seconds(update_interval)
    else:
        time_delay = update_interval
        time_seconds = update_interval
    update = data_scheduler.enter(time_delay, 1, update_covid_data, argument=(update_name,))
    covid_update = {
        'title': update_name,
        'content':"There is a covid update scheduled for " + str(update_interval),
        'update': update,
        'repeat': repeat,
        'timeSec': time_seconds,
        'time':update_interval,
        'type': "data"
    }
    return covid_update
