#!/usr/bin/python

""" Simple script for printing time in time zones I care about. """
from datetime import datetime, timedelta
from pytz import utc, timezone

fmt = '%Y-%m-%d %H:%M:%S %Z%z'

utc_time = utc.localize( datetime.utcnow() )

def localize_to_tz(tz):
    tz_time = utc_time.astimezone( timezone(tz) )
    return tz_time.strftime(fmt)

def print_timezone(location, tz):
    loc = location + " time:"
    print "{:27} {}".format(loc, localize_to_tz(tz) )

# To get a list of time zones: https://en.wikipedia.org/wiki/List_of_tz_zones_by_name
print_timezone("Ottawa", 'US/Eastern')
print_timezone("Philippine", 'Asia/Manila')
print_timezone("England", 'Europe/London')
print_timezone("UTC", 'Etc/UTC')
print("-----")
print_timezone("Tokyo", 'Asia/Tokyo')
print_timezone("Kolkata", 'Asia/Kolkata')
print_timezone("Karachi (Pakistan)", 'Asia/Karachi')
print_timezone("Paris", 'Europe/Paris')
print("-----")
print_timezone("Halifax (Nova Scotia)", 'Canada/Atlantic')
print_timezone("Winnipeg (Manitoba)", 'Canada/Central')
print_timezone("Regina (Saskatchewan)", 'Canada/Saskatchewan')
print_timezone("Calgary", 'Canada/Mountain')
print_timezone("Vancouver (BC)", 'Canada/Pacific')
