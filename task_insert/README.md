# task_insert

Command-line application for insert default tasks into a task list.
For the use case, where you have the same tasks for week day (log hours,
check mail, etc) and slightly different tasks for weekends.

Usage:
  $ python tasks,py

# INSTALLATION

## Get all dependencies

    `sudo apt-get install python-virtualenv python-dev build-essential`

## Create folder
    `sudo mkdir -p /data/pythonenv`

## Install dependencies

    `sudo pip install --upgrade google-api-python-client`


You will need to generate a clients_secrets.json file. It can be acquired by going to:
```
    Visit https://cloud.google.com/console/project
    Select "API project"
    Select "APIs & auth"
    Select "Credentials"
    Select "Download JSON"
    Copy and save to the root of this file and make sure its named clients_secrets.json
```

# CONFIGURATION

* modify TASKS_LISTS_TO_FOLLOW to the name of the task list that you
  want to insert tasks into
* modify WEEKDAY_TASK to list tasks that you wanted listed for weekdays
* modify WEEKEND_TASK for your weekend tasks.
