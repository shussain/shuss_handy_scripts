#!/usr/bin/env python

"""
Script that outputs the day's forecast. It uses the Canadian government's
weather info for the daily forecast.

Requirement
    sudo apt-cache show python-beautifulsoup

Script to use it:
    getweather.py > /tmp/weather.txt; mailx -s weather [email]  < /tmp/weather.txt
"""

from datetime import datetime, timedelta
import urllib2
from bs4 import BeautifulSoup

site='http://dd.weather.gc.ca/citypage_weather/xml/ON/s0000430_e.xml'
page = urllib2.urlopen(site)
soup = BeautifulSoup(page, "html.parser")

today = datetime.now() # + timedelta(days=1)
today_title = today.strftime('%A')

forecasts = soup.findAll('forecast')

for forecast in forecasts:
    period = forecast('period')[0].string
    if period.startswith(today_title):
        textsummary = forecast('textsummary')[0].string
        temperature = forecast('temperatures')[0]('textsummary')[0].string
        print(period)
        print(textsummary)
        print(temperature)
        print("-----")

