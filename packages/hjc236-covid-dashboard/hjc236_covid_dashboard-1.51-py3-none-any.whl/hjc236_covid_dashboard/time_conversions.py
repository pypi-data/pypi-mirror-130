"""
Contains functions for converting time between different formats

Functions:
    minutes_to_seconds()
    hours_to_minutes()
    hhmm_to_seconds()
    current_time_seconds()
"""

import time


def minutes_to_seconds(minutes: str) -> int:
    """Converts minutes to seconds"""
    return int(minutes) * 60


def hours_to_minutes(hours: str) -> int:
    """Converts hours to minutes"""
    return int(hours) * 60


def hhmm_to_seconds(hhmm: str) -> int:
    """Converts a string in the format hh:mm to a time in seconds from 00:00"""
    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
           minutes_to_seconds(hhmm.split(':')[1])


def current_time_seconds() -> int:
    """Returns the current time from 00:00 in seconds"""
    hhmm = str(time.gmtime().tm_hour) + ":" + str(time.gmtime().tm_min)
    seconds = hhmm_to_seconds(hhmm)
    return seconds
