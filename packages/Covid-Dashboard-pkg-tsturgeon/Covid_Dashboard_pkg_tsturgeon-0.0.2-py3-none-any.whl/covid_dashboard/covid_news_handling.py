"""
A python module for Tom Sturgeon Computer Science Coursework

Functions:
    news_API_request(Covid_terms:str="Covid COVID-19 coronavirus):
        - Requests data from the news Api
        - Filters the searches based on the string parsed to the function
        - Stores the returned articles in a global variable

    update_news_articles(name:str = 'init'):
        - calls news_API_request()
        - adds a parsed name to the end of the list
        - parsed name used to remove the scheduled event that called the function

    update_news(update_interval:str, update_name:str, repeat:bool = False):
        - uses the sched module to set an update
        - The delay is set for the time interval parsed
        - Returns a dictionary

    check_list(dict_list:list, value:str):
        - Takes a list of dictionaries
        - searches the list to see if a single title value is in it
        - returns the index of the item

    remove_news(headline:str, articles:list):
        - Calls check_list()
        - Removes the item at that index
        - Returns that item
"""
import json
import sched
import time
import logging
from datetime import datetime as dt
import requests
from .shared_functions import time_to_update_interval, time_to_seconds

with open('config.json', 'r', encoding="utf8") as file:
    config_data = json.load(file)

news_scheduler = sched.scheduler(time.time, time.sleep)
logging.basicConfig(filename=config_data['logging_file'], encoding='utf-8', level=logging.INFO)

news_reports = []

def news_API_request(covid_terms:str=config_data['search']['Search_Terms']):
    """ A function to request data from the news API """
    logging.info("News articles request at " + dt.fromtimestamp(time.time()).strftime('%c'))
    terms = covid_terms.lower().split(" ")
    news_articles = []

    for term in terms:
        search_criteria = {
            'apiKey': config_data['API_Key'],
            'qInTitle': term,
            'language': 'en',
            'sortBy':'popularity'
            }
        news_request = requests.get(
            "https://newsapi.org/v2/everything",
            search_criteria)
        news_response = news_request.json()
        news_articles += news_response["articles"]

    if len(news_articles) < 1:
        logging.warning("Unsuccsesful gathering of news stories")

    return news_articles

def news_data_return():
    """ A function to pass news articles to another python document """
    return news_reports

def update_news_articles( search_terms:str=config_data['search']['Search_Terms'],name:str = 'init'):
    """
    A function to get a list of news articles

    Adds the name of the scheduled event to the end of the list
    """
    global news_reports
    news_reports = news_API_request(search_terms)
    news_reports.append(name)


def update_news(
    update_interval:str,
    update_name:str,
    search_terms:str = config_data['search']['Search_Terms'],
    repeat:bool = False
    ):
    """
    A function to schedule news updates

    Returns a dictionary containing:
    - Title: Update name given by the user
    - Content: what and when the update is for
    - Update: The update Sched object
    - Repeat: Boolean value for weather it repeats or not
    - TimeSec: The time delay in seconds
    - Time: The time of the update to complete
    - Type: Weather its a news update or data
    """
    if isinstance(update_interval,str):
        time_delay = time_to_update_interval(update_interval)
        time_seconds = time_to_seconds(update_interval)
    else:
        time_delay = update_interval
        time_seconds = update_interval

    logging.info("Scheduled an update to the news for " + str(update_interval))
    update = news_scheduler.enter(time_delay, 1, update_news_articles, argument = (update_name,search_terms,))
    news_update = {
        'title': update_name,
        'content':'There is a news update scheduled for ' + str(update_interval),
        'update': update,
        'repeat': repeat,
        'timeSec': time_seconds,
        'time':update_interval,
        'type': "news"
    }
    return news_update

def check_list(dict_list:list, value:str):
    """ A function to find the index of a headline in a list of dictionary """
    for entry in dict_list:
        if entry['title'] ==  value:
            return dict_list.index(entry)

def remove_news(headline:str, articles:list):
    """
    A function to find the item to be deleted

    Returns the dictonary
    """
    logging.info("Looking for article to remove")
    index = check_list(articles, headline)
    if type(index) == int:
        del_item = articles.pop(index)
        logging.info("removed requested item")
        return del_item
    logging.info("Article not found")
    