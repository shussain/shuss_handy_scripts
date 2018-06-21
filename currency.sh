#!/bin/bash

# Get various conversion rate by scraping Google search.
#
# Ideally this would make API calls but the API and usage rules for'
# most currency conversion sites is far from ideal


GOOGLE_FINANCE="https://www.google.com/search?q=$1+to+$2"
AGENT="Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3"
BEGINING="s/<!doctype.*\J7UKTe\">//g"
ENDING='s/<\/div.*//'

getCurrency () {
    wget "$GOOGLE_FINANCE" -U $AGENT -o /dev/null -O /dev/stdout | sed -e $BEGINING | sed -e $ENDING | head -n 1
}

getCurrency "CAD" "USD"
getCurrency "USD" "CAD"
getCurrency "CAD" "PHP"
getCurrency "CAD" "INR"
getCurrency "CAD" "PKR"
getCurrency "CAD" "JPY"
getCurrency "BTC" "CAD"
getCurrency "GBP" "CAD"
getCurrency "EUR" "CAD"
