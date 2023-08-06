# -*- coding: utf-8 -*-
"""
Main functionality of the interface
"""
import json
import logging
import time
from datetime import datetime
from flask import Flask, request, render_template, redirect

from covid_data_handler import schedule_covid_updates
from covid_data_handler import covid_scheduler

from covid_news_handling import schedule_news_updates
from covid_news_handling import news_scheduler

with open('config.json') as config_file:
    config_data = json.load(config_file)

logging.basicConfig(filename='app_log.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)


removed_articles = []
scheduled_updates = []
repeated_updates = []


def time_to_interval(update_time: str) -> int:
    """
    Takes the the time of update and calculates the amount of seconds until the
    update must happen.

    Parameters
    ----------
    update_time : str
        DESCRIPTION. The time in 24hr format 'hh:mm'

    Returns
    -------
    int
        DESCRIPTION. Interval in seconds

    """
    current_time = time.strftime('%H:%M')
    time_diff = datetime.strptime(update_time, '%H:%M') -\
        datetime.strptime(current_time, '%H:%M')

    if time_diff.days < 0:
        interval = time_diff.total_seconds() + 86400
    else:
        interval = time_diff.total_seconds()

    return int(interval)


def get_covid_data() -> dict:
    """
    Processes the data from the json file where covid data is stored and
    returns this as a python dictionary

    Returns
    -------
    dict
        DESCRIPTION. Contains local last7days_cases, national last7days_cases,
        current_hospital_cases, total_deaths

    """

    with open('covid_data.json') as file:
        data = json.load(file)

    return data


def get_news_articles() -> list[dict]:
    """
    Processes the data from the json file where news data is stored and doesn't
    allow removed articles from dashboard to be added to the list of news data.

    Returns
    -------
    list
        DESCRIPTION. Contains dictionaries containing the headline, content and
        url of the news article.

    """

    with open('news_data.json') as file:
        news = json.load(file)

    for i in removed_articles:
        for index, item in enumerate(news):
            if i in item['title']:
                del news[index]
                break

    return news


def check_updates():
    """
    This is where the program checks if updates are finished then removes them,
    unless they need to be repeated then it repeates them.

    """
    for item in scheduled_updates:
        if item['event'] not in covid_scheduler.queue and\
             item['event'] not in news_scheduler.queue:
            if item in repeated_updates:
                update_time = item['time']
                interval = time_to_interval(update_time)
                update_lable = item['title']
                if item['type'] == 'Covid':
                    logging.info('Repeating covid update: %s', item['title'])
                    scheduled_update = schedule_covid_updates(interval,
                                                              update_lable)
                if item['type'] == 'News':
                    logging.info('Repeating news update: %s', item['title'])
                    scheduled_update = schedule_news_updates(interval,
                                                             update_lable)
                scheduled_update['repeat'] = True
                scheduled_update['content'] += \
                    ' Update time: ' + update_time
                scheduled_update['content'] += \
                    ' Repeat update: Yes'
                scheduled_update['time'] = update_time
                scheduled_updates.remove(item)
                scheduled_updates.append(scheduled_update)
                repeated_updates.remove(item)
                repeated_updates.append(scheduled_update)
            else:
                logging.info('Removing update: %s', item['title'])
                scheduled_updates.remove(item)


def remove_update_request():
    """
    Checks if the update has been removed froom the dashboard

    """
    update_lable = request.args.get('update_item')
    for item in scheduled_updates:
        if update_lable == item['title']:
            event = item['event']
            logging.info('User removing %s update: %s',
                         item['type'], item['title'])
            scheduled_updates.remove(item)
            if item['repeat']:
                repeated_updates.remove(item)
            if item['type'] == 'Covid':
                logging.info('Removing update %s from covid scheduler',
                             item['title'])
                covid_scheduler.cancel(event)
            if item['type'] == 'News':
                logging.info('Removing update %s from news scheduler',
                             item['title'])
                news_scheduler.cancel(event)


def remove_news_articles():
    """
    Checks if a news article has been removed

    """
    article_to_remove = request.args.get('notif')

    if article_to_remove:
        logging.info('Removing article: %s', article_to_remove)
        removed_articles.append(article_to_remove)


def covid_update_request():
    """
    Checks if a covid data update has been requested, if so, then checks if it
    needs to be scheduled and repeated.

    """
    update_time = request.args.get('update')
    update_lable = request.args.get('two')
    repeat = request.args.get('repeat')
    update_covid = request.args.get('covid-data')

    if update_covid:
        if update_time:
            interval = time_to_interval(update_time)
            logging.info('Scheduling covid update: %s', update_lable)
            scheduled_update = schedule_covid_updates(interval,
                                                      update_lable)
            scheduled_update['content'] += \
                ' Update time: ' + update_time
            scheduled_update['time'] = update_time
            if repeat:
                scheduled_update['repeat'] = True
                scheduled_update['content'] += \
                    ' Repeat update: Yes'
                logging.info('Adding %s to repeated updates', update_lable)
                repeated_updates.append(scheduled_update)
            else:
                scheduled_update['repeat'] = False
                scheduled_update['content'] += \
                    ' Repeat update: No'
            scheduled_updates.append(scheduled_update)
        else:
            logging.warning('Unable to update: No time given for covid update')


def news_update_request():
    """
    Checks if news data update has been requested, if so, then checks if it
    needs to be scheduled and repeated.

    """
    update_time = request.args.get('update')
    update_lable = request.args.get('two')
    repeat = request.args.get('repeat')
    update_news_articles = request.args.get('news')

    if update_news_articles:
        if update_time:
            interval = time_to_interval(update_time)
            logging.info('Scheduling news update: %s', update_lable)
            scheduled_update = schedule_news_updates(interval,
                                                     update_lable)
            scheduled_update['content'] += \
                ' Update time: ' + update_time
            scheduled_update['time'] = update_time
            if repeat:
                scheduled_update['repeat'] = True
                scheduled_update['content'] += \
                    ' Repeat update: Yes'
                logging.info('Adding %s to repeated updates', update_lable)
                repeated_updates.append(scheduled_update)
            else:
                scheduled_update['repeat'] = False
                scheduled_update['content'] += \
                    ' Repeat update: No'
            scheduled_updates.append(scheduled_update)
        else:
            logging.warning('Unable to update: No time given for covid update')


@app.route('/')
def rerutn_to_dash():
    """
    Redirects the page to '/index'

    """
    return redirect('/index')


@app.route('/index')
def dashboard():
    """
    Deals with requests from the webiste and executes these then returns the
    relevant data for the webpage to be refreshed.

    Returns
    -------
    The html file with relevant data

    """

    covid_scheduler.run(blocking=False)
    news_scheduler.run(blocking=False)

    covid_data = get_covid_data()
    national_last7days_cases = covid_data.get('last7days_cases')
    current_hospital_cases = covid_data.get('current_hospital_cases')
    total_deaths = covid_data.get('total_deaths')
    local_last7days_cases = covid_data.get('local_last7days_cases')

    check_updates()
    remove_update_request()
    remove_news_articles()

    update_lable = request.args.get('two')
    add = True
    for item in scheduled_updates:
        if update_lable == item['title']:
            logging.warning('Unable to add update: Lable already in use - %s',
                            update_lable)
            add = False
    if add:
        covid_update_request()
        news_update_request()

    return render_template('index.html',
                           image='image.jpg',
                           favicon='favicon.ico',
                           title='Daily Updates',
                           location=config_data['NATIONAL_LOCATION'],
                           local_7day_infections=local_last7days_cases,
                           nation_location=config_data['NATIONAL_LOCATION'],
                           national_7day_infections=national_last7days_cases,
                           hospital_cases='Current Hospital Cases: ' +
                           current_hospital_cases,
                           deaths_total='Total Deaths: '+total_deaths,
                           updates=scheduled_updates,
                           news_articles=get_news_articles()
                           )


if __name__ == '__main__':
    app.run()
