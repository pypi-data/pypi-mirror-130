"""
A python module for Tom Sturgeons Computer Science coursework

Functions:
    time_to_second(str_time: str):
        - Converts time from 'HH:MM:SS' to a number of seconds
        - Returns the number of seconds

    time_to_update_interval(alarm_time:str):
        - Calculates the number of seconds until the time provided is reached
"""

import time
from datetime import datetime as dt

def time_to_seconds(str_time: str):
    """ Convert 'HH:MM:SS' to seconds """
    unformated_time = str_time.split(":")
    wanted_hour = int(unformated_time[0])*60*60
    wanted_minute = int(unformated_time[1])*60
    if len(unformated_time)>2:
        wanted_second = int(unformated_time[2])
    else:
        wanted_second = 0
    formated_time = wanted_hour + wanted_minute + wanted_second
    return formated_time

def time_to_update_interval(alarm_time:str):
    """Converts the time for normal format to a number of seconds until that time arives"""
    # Convert the alarm time into seconds
    wanted_time = time_to_seconds(alarm_time)

    # Selects the correct time feature
    current_time = dt.fromtimestamp(time.time()).strftime('%c')
    unformated_current_time = current_time.split(" ")
    index = 0
    while ":" not in unformated_current_time[index]:
        index += 1

    # Converts current time into seconds
    unformated_current_time = unformated_current_time[index]
    wanted_currnent_time = time_to_seconds(unformated_current_time)
    #  Calculates how many seconds until the alarm is needed
    update_interval = wanted_time-wanted_currnent_time
    if update_interval < 0:
        update_interval += 24*60*60
    return update_interval
