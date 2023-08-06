"""
 The main python document for Tom Sturgeon's coursework

This document runs the web server for the covid dashboard

Functions:
    update_covid_sched(update_time, name,repeat):
        - Adds a new scheduler object to the scheduled_updates list to get new covid data
        - If the update time is the same as another update time then no new update is added

    update_news_sched(update_time, name,repeat):
        - Adds a new scheduler object to the scheduled_updates list to get new news articles
        - if the update time is the same as another update time then no new update is added
"""

import logging
import json
from flask import Flask, render_template, request, Markup
#from string import Template
#from datetime import datetime as dt
from .covid_data_handler import (
    covid_data_return,
    update_covid_data,
    schedule_covid_updates,
    data_scheduler
)
from .covid_news_handling import(
    news_data_return,
    update_news_articles,update_news,
    remove_news,
    news_scheduler
)

with open('config.json', 'r', encoding="utf8") as file:
    config_file = json.load(file)

app = Flask(__name__)

logging.basicConfig(filename=config_file['logging_file'], encoding='utf-8', level=logging.INFO)


scheduled_updates = []
del_news = []

update_covid_data()
update_news_articles()


def update_covid_sched(update_time:str, name:str,repeat:bool):
    """Function to call for an update of covid data"""
    logging.info("Webpage requesting Covid data update")
    new_data = schedule_covid_updates(update_time, name,repeat)
    add_update = True
    for update in scheduled_updates:
        if new_data['timeSec'] == update['timeSec'] and new_data['type'] == update['type']:
            add_update = False
    if add_update is True:
        scheduled_updates.append(new_data)

def update_news_sched(update_time:str, name:str, repeat:bool):
    """A function to call for an update of news articles"""
    logging.info("Webpage requesting News update")
    new_news = update_news(update_time, name, repeat, config_file['search']['Search_Terms'])
    add_update = True
    for update in scheduled_updates:
        if new_news['timeSec'] == update['timeSec'] and new_news['type'] == update['type']:
            add_update = False
    if add_update is True:
        scheduled_updates.append(new_news)

def remove_del_news_articles(news:list):
    """ Removes all deleted articles from the news list"""
    #news = news_data_return()
    index = 0
    for article in news:
        if article in del_news:
            logging.info("Removing deleted articles from choice of news")
            del news[index]
            index -= 1
        index += 1
    return news

def add_hyperlink(news:list):
    """ Adds a hyperlink to the title of the news article"""
    for index in range(len(news)):
        new_title = f"<a href={news[index]['url']}> {news[index]['title']} </a>"
        news[index]['title'] = Markup(new_title)
        #print(news[index]['title'])
    return news



def remove_updates(update_name:str ,overwrite_repeat:bool = False):
    """ Removes updates from the scheduled updates list"""
    logging.info("looking for scheduled update to remove")
    repeat_data = False
    repeat_news = False
    for update in scheduled_updates:
        if update['title'] == update_name:
            if update['repeat'] is True:
                if update['type'] == 'data':
                    repeat_data = True
                    data_data = update
                if update['type'] == 'news':
                    repeat_news = True
                    news_data = update

            scheduled_updates.remove(update)
            logging.info("Scheduled update removed")
    if overwrite_repeat is True:
        return scheduled_updates
    if repeat_data is True:
        update_covid_sched(data_data['time'], data_data['title'], data_data['repeat'])
        logging.info("Repeat data update rescheduled for " + update['time'])
        data_data = ""
    if repeat_news is True:
        update_news_sched(news_data['time'], news_data['title'], news_data['repeat'])
        logging.info("Repeat news update rescheduled for " + update['time'])
        news_data = ""
    return scheduled_updates


@app.route("/")
@app.route("/index")
def webpage():
    """A function to recieve and send data to the HTML document"""
    logging.info("Running webpage loop")
    data_scheduler.run(blocking=False)
    news_scheduler.run(blocking=False)
    news = news_data_return()
    news = remove_del_news_articles(news)
    news_update_to_remove = news.pop()
    remove_updates(news_update_to_remove)
    covid_data = covid_data_return()
    data_update_to_remove = covid_data['remove']
    remove_updates(data_update_to_remove)
    formatted_hospital_cases = "National Hospital Cases: " + str(covid_data["hospitalCases"])
    formatted_death_total = "National Death Total: " + str(covid_data['totalDeaths'])
    text_field = request.args.get('two')
    update_time = request.args.get('update')
    covid_update = request.args.get('covid-data')
    news_update = request.args.get('news')
    close_news_headline = request.args.get('notif')
    cancel_update = request.args.get('update_item')
    repeat = request.args.get('repeat')
    if cancel_update:
        ignore_repeat = True
        remove_updates(cancel_update, ignore_repeat)
    if text_field:
        repeat_update = False
        if repeat:
            repeat_update = True
        if covid_update:
            update_covid_sched(update_time, text_field,repeat_update)
        if news_update:
            update_news_sched(update_time, text_field,repeat_update)
    if close_news_headline:
        del_news.append(remove_news(close_news_headline, news))

    return render_template(
        "index.html",
        title=config_file['template']['dashboard_title'],
        image = config_file['template']['image'],
        favicon = config_file['template']['favicon'],
        news_articles = add_hyperlink(news[0:5]),
        local_7day_infections = covid_data['local7Days'],
        national_7day_infections = covid_data['nation7Days'],
        hospital_cases = formatted_hospital_cases,
        deaths_total = formatted_death_total,
        updates = scheduled_updates
    )

if __name__ == "__main__":
    app.run()
