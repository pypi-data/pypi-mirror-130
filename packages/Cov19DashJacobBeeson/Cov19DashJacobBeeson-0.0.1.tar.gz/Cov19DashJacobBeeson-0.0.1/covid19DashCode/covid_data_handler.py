# -*- coding: utf-8 -*-
"""
All the Covid data handling functionality
"""
import csv
import sched
import time
import json
import logging
from uk_covid19 import Cov19API

with open('config.json') as config_file:
    config_data = json.load(config_file)

covid_scheduler = sched.scheduler(time.time, time.sleep)

logging.basicConfig(filename='app_log.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


def parse_csv_data(csv_filename: str) -> list:
    """
    Reads a csv file and then returns a list of strings for each of the rows in
    the file.

    Parameters
    ----------
    csv_filename : str

    Returns
    -------
    list

    """
    with open(csv_filename) as file:
        csvreader = csv.reader(file)
        data = []
        for row in csvreader:
            data.append(row)

    return data


def process_covid_csv_data(covid_csv_data: list) -> int:
    """
    takes a list of data that is returned from the function 'parse_csv_data'
    and then returns three variables

    last7days_cases is Calculated by summing the new cases by specimen date for
    the last 7 days ignoring the first entry as data is incomplete

    Parameters
    ----------
    covid_csv_data : list

    Returns
    -------
    int
        DESCRIPTION. Order of return: last7days_cases, current_hospital_cases,
        total_deaths

    """
    last7days_cases = 0
    for i in range(3, 10):
        last7days_cases = last7days_cases + int(covid_csv_data[i][6])
    current_hospital_cases = int(covid_csv_data[1][5])
    total_deaths = int(covid_csv_data[14][4])
    return last7days_cases, current_hospital_cases, total_deaths


def covid_API_request(location: str = 'Exeter', location_type: str = 'ltla')\
        -> dict:
    """
    Uses Cov19API from the uk_covid19 module to request information from the
    specified location.

    Parameters
    ----------
    location : str, optional
        DESCRIPTION. The default is 'Exeter'.
    location_type : str, optional
        DESCRIPTION. The default is 'ltla'.

    Returns
    -------
    dict
        DESCRIPTION. Up-to-date Covid data

    """

    last7days_cases = 0
    covid_data_dict = {}

    england_only = [
        'areaType='+location_type,
        'areaName='+location
    ]
    cases_and_deaths = {
        "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate",
    }

    api = Cov19API(filters=england_only, structure=cases_and_deaths)
    request = api.get_json()
    covid_data = request.get('data')
    i = 0
    try:
        for i in range(7):
            last7days_cases = last7days_cases +\
                covid_data[i]['newCasesBySpecimenDate']
    except TypeError:
        while covid_data[i]['newCasesBySpecimenDate'] is None:
            if i < len(covid_data)-8:
                i = i+1
                try:
                    for i in range(i, i+7):
                        last7days_cases = last7days_cases +\
                            covid_data[i]['newCasesBySpecimenDate']
                except TypeError:
                    logging.warning('Trouble calculating last7days_cases')
            else:
                last7days_cases = 'Unable to get data'
                break

    i = 0
    while covid_data[i]['hospitalCases'] is None:
        if i < len(covid_data)-1:
            i = i+1
        else:
            break
    current_hospital_cases = covid_data[i]['hospitalCases']

    i = 0
    while covid_data[i]['cumDailyNsoDeathsByDeathDate'] is None:
        if i < len(covid_data)-1:
            i = i+1
        else:
            break

    total_deaths = covid_data[i]['cumDailyNsoDeathsByDeathDate']

    covid_data_dict['last7days_cases'] = str(last7days_cases)
    covid_data_dict['current_hospital_cases'] = str(current_hospital_cases)
    covid_data_dict['total_deaths'] = str(total_deaths)

    return covid_data_dict


def update_covid_data():
    """
    Where the json file containing the covid data is updated by calling the
    covid_API_request for both national and local locations.

    Returns
    -------
    None.

    """
    covid_data = covid_API_request(config_data['NATIONAL_LOCATION'], 'nation')
    local_data = covid_API_request(config_data['LOCAL_LOCATION'], 'ltla')
    covid_data['local_last7days_cases'] = local_data.get('last7days_cases')

    json_data = json.dumps(covid_data)
    with open("covid_data.json", "w") as file:
        file.write(json_data)


def schedule_covid_updates(update_interval: int, update_name: str) -> dict:
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
        update. Also the type of update to differentiate from a news update
        with the same title

    """
    sched_updates = {}
    event = covid_scheduler.enter(update_interval, 1, update_covid_data)

    sched_updates['title'] = update_name
    sched_updates['content'] = 'Covid data update!'
    sched_updates['event'] = event
    sched_updates['type'] = 'Covid'

    return sched_updates
