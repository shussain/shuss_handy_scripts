#!/usr/bin/env python

"""
Preparation
    sudo apt-get install python-beautifulsoup

Script to use it:
    getamazon.py > /tmp/weather.txt; mailx -s 'amazon prices'  habibilus@gmail.com < /tmp/weather.txt
"""

from time import sleep
import urllib2
from BeautifulSoup import BeautifulSoup

site='http://www.amazon.ca/gp/product/'

def try_get_price(soup, attr_type, attr_value):
    price = None

    try:
        price = soup.find("span", attrs={attr_type: attr_value}).string
    except:
        pass

    return price


def getprice(description, contentlink):
    page  = urllib2.urlopen(site+contentlink)
    soup  = BeautifulSoup(page)

    price = try_get_price(soup, "id", "priceblock_ourprice")
    if not price: price = try_get_price(soup, "id", "priceblock_dealprice")
    if not price: price = try_get_price(soup, "id", "priceblock_saleprice")
    if not price: price = try_get_price(soup, "class", "a-size-medium a-color-price offer-price a-text-normal");

    try:
        print description + ": " + price
    except:
        print("%s could not get price" % description)
    sleep(5)

# Amazon needs cookie for getting resources
urllib2.urlopen('http://www.amazon.ca')

# Get actual items. Format should be:
# description, item price
# e.g.  Kenneth cole New York watch, B017WS9NT6

f = open('/home/habibilus/bin/amazon_price.txt', 'r')
for line in f:
    #print line
    description, contentlink = line.split(',')
    description = description.strip()
    contentlink = contentlink.strip()
    getprice(description, contentlink)

