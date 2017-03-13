#!/usr/bin/python
#
# Get the time delta for hours.
# Usage: timedelta.py  145.5
#
# get workdays: pip install workdays

from datetime import date, datetime,timedelta
from workdays import networkdays
import sys

HOUR_PER_DAY = 8
PERCENTAGE = 0.1    # 0.1 = 10%; 0.2 = 20%

if len(sys.argv) < 2:
    print "Pass number of hours worked"
    sys.exit(1)

hours_done = float( sys.argv[1] )

currentDate  = date.today()
firstOfMonth = date(currentDate.year, currentDate.month, 1)

days = networkdays(firstOfMonth, currentDate)
expected_hour = days * HOUR_PER_DAY

percentage_delta = (expected_hour - hours_done) / hours_done
time_delta = ( expected_hour / (1+PERCENTAGE) ) - hours_done

print("percentage_delta = %0.4f" % percentage_delta)
print("time delta (Positive is time owed to company) = %0.4f" % time_delta)
