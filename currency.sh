#!/bin/bash

# Get various conversion rate from open exchange rates
curl -X GET -s https://openexchangerates.org/api/latest.json\?app_id\=ID_STRING > /tmp/currency.txt
egrep "CAD|PHP|INR|PKR|JPY|GBP|EUR|BTC"  /tmp/currency.txt
