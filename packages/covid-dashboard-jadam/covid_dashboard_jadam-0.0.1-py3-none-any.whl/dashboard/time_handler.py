'''This module handles conversion between various time formats, as well
   as importing the current time'''
import time
import logging

from covid_data_handler import FORMAT

logging.basicConfig(format=FORMAT,filename='system.log',level=logging.INFO)

def minutes_to_seconds(minutes: str) -> int:
    '''converts minutes to seconds'''
    return int(minutes)*60

def hours_to_seconds(hours: str) -> int:
    '''converts hours to seconds'''
    return int(hours)*3600

def hhmm_to_seconds(hhmm: str) -> int:
    '''converts time from the form hh:mm into seconds'''
    return (hours_to_seconds(hhmm.split(':')[0]) +\
            minutes_to_seconds(hhmm.split(':')[1]))

def current_time_hhmm():
    '''returns the current time in form hh:mm'''
    return str(time.gmtime().tm_hour) + ':' + str(time.gmtime().tm_min)

def seconds_to_set_time(set_time: str) -> int:
    '''takes in a time in the form hh:mm and returns the number of seconds
       between the current time and then'''
    logging.debug('seconds_to_set_time triggered')
    if hhmm_to_seconds(current_time_hhmm()) <= hhmm_to_seconds(set_time):
        return hhmm_to_seconds(set_time) -\
               hhmm_to_seconds(current_time_hhmm())
    else:
        return hhmm_to_seconds(set_time) -\
               hhmm_to_seconds(current_time_hhmm()) + hhmm_to_seconds('24:00')
