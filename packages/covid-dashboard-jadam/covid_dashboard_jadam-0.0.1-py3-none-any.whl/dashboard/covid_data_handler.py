'''This module handles importing and sorting covid data
for the United Kingdom'''
import json
import sched
import time
import logging

from uk_covid19 import Cov19API


s = sched.scheduler(time.time, time.sleep)
FORMAT='%(levelname)s:%(asctime)s:%(message)s'
logging.basicConfig(format=FORMAT,filename='system.log',level=logging.DEBUG)

def get_config_data(config_filename):
    '''opens the configuration file and returns it as a dictionary
       arguments: config_filename: a file containg configuartion data'''

    logging.debug('get_config_data triggered')

    with open(config_filename, 'r') as myfile:
        config_data = myfile.read()

    return json.loads(config_data)

config = get_config_data('config.json')

def parse_csv_data(csv_filename):
    '''takes in a csv file and returns it as a list
       arguments: csv_filename: a csv file'''

    logging.debug('parse_csv_data triggered')

    lines = open(csv_filename, 'r').readlines()
    return lines

def process_covid_csv_data(covid_csv_data: list) -> str:
    '''takes in a list of covid data and returns strings of data
       arguments: covid_csv_data: a list of covid data for specified days'''

    logging.debug('process_covid_csv_data triggered')

    total_deaths = -1
    current_hospital_cases = -1
    last7days_cases = -1
    index = 0

    for i in range (0, len(covid_csv_data[0].split(','))):
        if covid_csv_data[0].split(',')[i].strip('\n') ==\
           'cumDailyNsoDeathsByDeathDate':
            total_deaths_index = i
        elif covid_csv_data[0].split(',')[i].strip('\n') == 'hospitalCases':
            hospital_cases_index = i
        elif covid_csv_data[0].split(',')[i].strip('\n') ==\
             'newCasesBySpecimenDate':
            new_cases_index = i

    while total_deaths == -1 or current_hospital_cases == -1 or\
          last7days_cases == -1:
        index += 1
        if covid_csv_data[index].split(',')[total_deaths_index].strip('\n')\
           != '' and total_deaths == -1:
            total_deaths = int(covid_csv_data[index].split(',')[4])

        if covid_csv_data[index].split(',')[hospital_cases_index].strip('\n')\
           != '' and current_hospital_cases == -1:
            current_hospital_cases = int(covid_csv_data[index].split(',')[5])

        if covid_csv_data[index].split(',')[new_cases_index].strip('\n')\
           != '' and last7days_cases == -1:
            last7days_cases = 0
            for i in range (1,8):
                last7days_cases += int(covid_csv_data[index +\
                                                      i].split(',')[6])

    return (last7days_cases, current_hospital_cases, total_deaths)

def covid_API_request(location: str='Exeter', location_type: str='ltla')\
    -> dict:
    '''imports covid data from an API and returns a dictionary
       arguments: location: a string containing the location to retrieve
                            data for
                  location_type: a string containg the type of the location'''

    logging.debug('covid_API_request triggered')
    global covid_data
    last7days_cases = 0

    national_filters = [
        'areaType=Nation',
        'areaName='+config['nation']
    ]

    national_structure = {
        "hospitalCases": "hospitalCases",
        "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate"
    }

    new_cases_filters = [
        'areaType='+location_type,
        'areaName='+location
    ]

    new_cases_structure = {
        "newCasesByPublishDate": "newCasesByPublishDate"
    }

    api = Cov19API(filters=national_filters, structure=national_structure)
    national_data = api.get_json()

    api = Cov19API(filters=new_cases_filters, structure=new_cases_structure)
    new_cases_data = api.get_json()

    for i in range (0,7):
        last7days_cases += new_cases_data['data'][i]['newCasesByPublishDate']

    covid_data = {
                    'last7days_cases':last7days_cases,
                    'current_hospital_cases':national_data['data'][0]['hospitalCases'],
                    'total_deaths':national_data['data'][1]['cumDeaths28DaysByDeathDate']
                 }

    return covid_data

def schedule_covid_updates(update_interval: int, update_name: str) -> None:
    '''Schedules updates to the live_covid_data dictionary after the given
       interval
       Arguments: update_interval: an integer for the time in seconds before
                                   updates trigger
                  update_name: a string that names the update'''

    logging.debug('schedule_covid_updates triggered')
    update = s.enter(update_interval, 1, covid_API_request)
    s.run()
