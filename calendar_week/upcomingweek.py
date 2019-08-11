# -*- coding: utf-8 -*-
#
# Modified from Google sample site

""" Command-line application for getting upcoming week events from
    Google Calendar.

Usage:
  $ python upcomingweek.py

= INSTALLATION =

Get all dependencies
    sudo apt-get install python-virtualenv python-dev build-essential

Install dependencies
    pip install --upgrade google-api-python-client


cat runcalendar.sh
    #!/bin/bash

    python $HOME/code/python_code/calendar/upcomingweek.py

You will need to generate a clients_secrets.json file. It can be acquired by going to:
    Visit https://cloud.google.com/console/project
    Select "API project"
    Select "APIs & auth"
    Select "Credentials"
    Select "Download JSON"
    Copy and save to the root of this file and make sure its named clients_secrets.json


NOTE: Run this script at least once to ensure everything is running and the
permissions are defined. Afterwards, the cron job can deal with requests
"""

from __future__ import print_function
import httplib2
import os

import datetime
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_service():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Services, the obtained service.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    week events for the user's calendar (not just primary but all calendars)

    """
    service = get_service()

    now  = datetime.datetime.utcnow()
    week = now + datetime.timedelta(weeks = 1)

    # reformat it to approved format
    now  =  now.isoformat() + 'Z' # 'Z' indicates UTC time
    week = week.isoformat() + 'Z' # 'Z' indicates UTC time

    # Get a list of all calendars I follow
    calendar_list = service.calendarList().list(pageToken=None).execute()

    # Get calendar ID
    calendarID = list()
    for calendar_list_entry in calendar_list['items']:
        # For some of the Google specific calendar, they have
        # id of #. Lets ignore them (no sense in getting it's
        # weekly status
        if (calendar_list_entry['id'].find('#') != -1): continue
        calendarID.append( calendar_list_entry['id'] )
        # print(calendar_list_entry['id'])


    allevents = list()
    # Get events for all calendars
    for id in calendarID:
        eventsResult = service.events().list(
            calendarId=id, timeMin=now, timeMax=week, singleEvents=True,
            orderBy='startTime').execute()
        allevents.append( eventsResult.get('items', []) )

    if not allevents:
        print('No upcoming events found.')
        return

    print('Getting the upcoming weeks events')

    # intelligently store the results
    weeklyevents = list()
    for events in allevents:
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            if 'summary' in event.keys():
                weeklyevents.append(start + ' ' + event['summary'])

    weeklyevents.sort()
    for events in weeklyevents:
        events = events.encode('ascii', 'ignore').decode('ascii') # strip out accents
        print(events)

if __name__ == '__main__':
    main()

