# -*- coding: utf-8 -*-
"""
All the News data handling functionality
"""
import json
import sched
import time
import requests

with open('config.json') as config_file:
    config_data = json.load(config_file)

news_scheduler = sched.scheduler(time.time, time.sleep)


def news_API_request(covid_terms: str = "Covid COVID-19 coronavirus") -> dict:
    """
    Uses the requests module to get up-to-date news articles from the news api

    Parameters
    ----------
    covid_terms : str, optional
        DESCRIPTION. The default is "Covid COVID-19 coronavirus". Specific
        terms that must be contained with the news headline.

    Returns
    -------
    dict
        DESCRIPTION. Contains current news information

    """
    keywords = covid_terms.lower().split()
    keywords = " OR ".join(keywords)
    news_info = requests.get('https://newsapi.org/v2/everything?'
                             'language=' + config_data['LANGUAGE'] +
                             '&qInTitle=' + keywords +
                             '&apiKey=' + config_data['API_KEY'])
    # .text converts html codes into readable text
    # json.loads method converts json string to python dict
    request = json.loads(news_info.text)
    return request


def update_news(covid_terms: str = "Covid COVID-19 coronavirus"):
    """
    Where the json file containing the news information is updated by calling
    the news_API_request with the specified search terms.

    Parameters
    ----------
    covid_terms : str, optional
        DESCRIPTION. The default is "Covid COVID-19 coronavirus". To be passed
        to the news_API_request when called. Allows other terms to be used.

    Returns
    -------
    None.

    """

    news = []

    request_dict = news_API_request(covid_terms)
    news_articles = request_dict.get('articles')

    for item in news_articles:
        news_dict = {}
        news_dict['title'] = item['title']
        news_dict['content'] = item['content']
        news_dict['url'] = item['url']
        news.append(news_dict)

    json_data = json.dumps(news)
    with open("news_data.json", "w") as file:
        file.write(json_data)


def schedule_news_updates(update_interval: int, update_name: str) -> dict:
    """
    Enters the requested update to the shecduler at the specified time.

    Parameters
    ----------
    update_interval : int
        DESCRIPTION. Seconds scheduler will wait before executing
    update_name : str
        DESCRIPTION. Identifier for the update, as displayed on the dashboard

    Returns
    -------
    dict
        DESCRIPTION. Contains the title, content and the scheduler event of the
        update. Also the type of update to differentiate from a covid update
        with the same title
    """
    sched_updates = {}
    event = news_scheduler.enter(update_interval, 1, update_news)

    sched_updates['title'] = update_name
    sched_updates['content'] = 'News article update!'
    sched_updates['event'] = event
    sched_updates['type'] = 'News'

    return sched_updates
