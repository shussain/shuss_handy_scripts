#!/usr/bin/env python

"""
Script that outpust the day's forecast. It uses the Canadian government's
weather info for the daily forecast.

Requirement
    sudo apt-cache show python-beautifulsoup

Script to use it:
    getweather.py > /tmp/weather.txt; mailx -s weather [email]  < /tmp/weather.txt
"""

from datetime import datetime, timedelta
import urllib2
from BeautifulSoup import BeautifulSoup

site='http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000430_e.xml'
page = urllib2.urlopen(site)
soup = BeautifulSoup(page)

tomorrow = datetime.now() + timedelta(days=1)
tomorrow_title = tomorrow.strftime('%A')

forecasts = soup.findAll('forecast')

for forecast in forecasts:
    period = forecast('period')[0].string
    if period.startswith(tomorrow_title):
        textsummary = forecast('textsummary')[0].string
        temperature = forecast('temperatures')[0]('textsummary')[0].string
        print period
        print textsummary
        print temperature
        print "-----"

