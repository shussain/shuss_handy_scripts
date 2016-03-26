# -*- coding: utf-8 -*-
#
# Modified from Google sample site

""" Command-line application for inserting tasks.

Usage:
  $ python tasks,py

INSTALLATION
Get all dependencies
    sudo apt-get install python-dev build-essential

Install dependencies
    sudo pip install --upgrade google-api-python-client


cat runtasks_insert.sh

    #!/bin/bash

    python $HOME/code/python_code/tasks_insert/tasks_insert.py


You will need to generate a clients_secrets.json file. It can be acquired by going to:
    Visit https://cloud.google.com/console/project
    Select "API project"
    Select "APIs & auth"
    Select "Credentials"
    Select "Download JSON"
    Copy and save to the root of this file and make sure its named clients_secrets.json


"""

import argparse
import httplib2
import os, sys

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

import json
# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])


# CLIENT_SECRETS is name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret. You can see the Client ID
# and Client secret on the APIs page in the Cloud Console:
# <https://cloud.google.com/console#/project/507335852380/apiui>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

TASKS_LISTS_TO_FOLLOW = 'todo_d_daily'
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WEEKENDS = ["Saturday/Sunday"]

WEEKDAY_TASK = ["Read IETF email", "Read programming book",
                "Watch programming video", "Day focus: ", "Weekly focus: "]
WEEKEND_TASK = ["Saturday: Kid allowance", "Saturday: watch programming video",
                "Sunday: Plan for upcoming week", "Sunday: Write week report"]

# Reversing order since each newly inserted is at the top (that can
# change but it helps)
WEEKDAYS.reverse()
WEEKDAY_TASK.reverse()
WEEKEND_TASK.reverse()

# Set up a Flow object to be used for authentication.
# Add one or more of the following scopes. PLEASE ONLY ADD THE SCOPES YOU
# NEED. For more information on using scopes please see
# <https://developers.google.com/+/best-practices>.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/tasks',
      'https://www.googleapis.com/auth/tasks.readonly',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

def credentials():
  # Parse the command-line flags.
  flags = parser.parse_args(None)

  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  return http

def time_period(service, tasklist_id, day, events):
    task_day = { 'title' : day }
    d = service.tasks().insert(tasklist=tasklist_id, body=task_day).execute()
    print("Insert %s" % day)
    #print d

    d_id = d['id']

    for event in events:
        task_event = { 'title' : event }
        ev = service.tasks().insert(tasklist=tasklist_id, parent=d_id, body=task_event).execute()

def main(argv):

  http = credentials()
  # Construct the service object for the interacting with the Tasks API.
  service = discovery.build('tasks', 'v1', http=http)

  try:
    # Get tasklists
    request  = service.tasklists().list()
    response = request.execute()

    tasklist = response['items']
    tasklist_cnt = len( tasklist )

    tasklist_id = ''
    # Get the tasklist id that we are interested in.
    for i in range(tasklist_cnt):
        if tasklist[i]['title'] == TASKS_LISTS_TO_FOLLOW:
            tasklist_id = tasklist[i]['id']

    for day in WEEKENDS:
        time_period(service, tasklist_id, day, WEEKEND_TASK)
    for day in WEEKDAYS:
        time_period(service, tasklist_id, day, WEEKDAY_TASK)

  except client.AccessTokenRefreshError:
      print ("The credentials have been revoked or expired, please re-run"
            "the application to re-authorize")



if __name__ == '__main__':
  main(sys.argv)
