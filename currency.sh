#!/bin/bash

# Get various conversion rate from Google Finance

getCurrency () {
    GOOGLE_FINANCE="https://www.google.com/finance?q=$1$2"
    TEXT_GREP="1 $1 = .* $2"

    wget "$GOOGLE_FINANCE" -o /dev/null -O /dev/stdout|grep -e "$TEXT_GREP"|sed 's/<span class=bld>//'|sed 's/<.*>//g'
}

getCurrency "CAD" "USD"
getCurrency "USD" "CAD"
getCurrency "CAD" "PHP"
getCurrency "CAD" "INR"
getCurrency "CAD" "PKR"
getCurrency "CAD" "AUD"
getCurrency "BTC" "CAD"
getCurrency "GBP" "CAD"
getCurrency "EUR" "CAD"
