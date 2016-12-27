# -*- coding: utf-8 -*-

"""

 Command-line application for getting all email with 'Todo' label and
 insert it into a particular Google Task.

Usage:
  $ python todo.py

INSTALLATION
Get all dependencies
    sudo apt-get install python-virtualenv python-dev build-essential

Create folder
    sudo mkdir -p /data/pythonenv

Install dependencies
    pip install --upgrade google-api-python-client


cat runcalendar.sh
    #!/bin/bash

    python /home/shussain/code/python_code/todo/todo.py


cat /etc/cron.d/tasks

    # /etc/cron.d/anacron: crontab entries for the anacron package

    SHELL=/bin/bash
    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

    */5 * * * * shussain cd /home/shussain/code/python_code/todo/; ./todo.py

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

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/tasks.readonly',
          'https://www.googleapis.com/auth/tasks',]

CLIENT_SECRET_FILE = 'client_secrets.json'
APPLICATION_NAME = 'App for parsing gmail todo and insert it into task'


TASKS_LISTS_TO_FOLLOW = 'todo_d_daily'
LABELNAME='Todo'
LABELID='Label_138'

LABELREMOVETODOID='Label_140' # Label ID for 'readTodo' label

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'gmail-todoandtask.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def getLabelAndID(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
      for label in labels:
        if label['name']==LABELNAME:
            print( "%s: %s" % (label['name'],label['id']) )
        if label['name']=='readTodo':
            print( "%s: %s" % (label['name'],label['id']) )

def getspecificLabel(service):
    results = service.users().labels().get(userId='me',id=LABELID).execute()
    print('-----')
    print(results)
    label = results.get('label', [])
    print(label)

def getEmailWithLabel(service):
    emailList = list()

    results  = service.users().messages().list(userId = 'me',labelIds = LABELID,q="is:unread",includeSpamTrash = False).execute()
    messages = results.get('messages', [])
    # So we have all emails id with a given label. Now lets get the actual
    # email (so we can get subject and date
    for message in messages:
        result = service.users().messages().get(userId='me',id=message['id']).execute()
        headers = result['payload']['headers']
        for h in headers:
            if (h['name']=='Date'):     emailDate = h['value']
            if (h['name']=='Subject'):  subject   = h['value']

        emailList.append( {'emailID':message['id'],'Subject':subject, 'date':emailDate} )

    return emailList

# "Wed, 8 Feb 2012 16:03:30 -0500" , "%a, %d %b %Y %H:%M:%S -0500"

def getTaskListID(service):
    request  = service.tasklists().list()
    response = request.execute()

    tasklist = response['items']
    tasklist_cnt = len( tasklist )

    tasklist_id = ''
    # Get the tasklist id that we are interested in.
    for i in range(tasklist_cnt):
        if tasklist[i]['title'] == TASKS_LISTS_TO_FOLLOW:
            tasklist_id = tasklist[i]['id']

    return tasklist_id

def time_period(service, tasklist_id, subject):
    task_item = { 'title' : subject }
    d = service.tasks().insert(tasklist=tasklist_id, body=task_item).execute()
    print("Insert %s" % subject)

def trashEmail(service, emailID):
    result  = service.users().messages().trash(userId = 'me',id =emailID).execute()

def modifyEmail(service, emailID):
    bodyDict = { "removeLabelIds": [LABELID], "addLabelIds": [LABELREMOVETODOID] }
    result   = service.users().messages().modify(userId = 'me',id = emailID, body=bodyDict).execute()



def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())

    gmail_service = discovery.build('gmail', 'v1', http=http)
    task_service  = discovery.build('tasks', 'v1', http=http)


    tasklist_id = getTaskListID(task_service)
    #getLabelAndID(gmail_service)
    # getspecificLabel(gmail_service)
    emailList   = getEmailWithLabel(gmail_service)

    if not emailList: exit()

    for email in emailList:
        # Add email subject line to task list
        time_period(task_service, tasklist_id, email['Subject'])
        # relabel it to readTodo and then place it in the trash
        modifyEmail(gmail_service, email['emailID'])
        trashEmail(gmail_service, email['emailID'])


if __name__ == '__main__':
    main()
