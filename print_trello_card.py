# -*- coding: utf-8 -*-
#

""" Command-line application to print "Backlog" and "Doing" list in Reinhardt
    trello account.

Usage:
  $ python print_trello_cards,py

= INSTALLATION =

Install dependencies
    sudo pip install py-trello

= CONFIGURATION =

* modify API_KEY, API_SECRETS, BOARD, LIST_TO_PRINT


"""
from trello import TrelloClient

API_KEY        = ''
API_SECRET     = ''
BOARD          = u''
LISTS_TO_PRINT = [u'']

if not API_KEY:
    exit("Define API_KEY in order to use this script")
elif not API_SECRET:
    exit("Define API_SECRET in order to use this script")
elif not BOARD:
    exit("Define BOARD in order to use this script")
elif not LISTS_TO_PRINT:
    exit("Define LISTS_TO_GRAB in order to use this script")

client = TrelloClient(
    api_key=API_KEY,
    api_secret=API_SECRET
)


def get_particular_item(trello_objects, name):
  returnedItem = None
  for trello_object in trello_objects:
    if trello_object.name == name:
      returnedItem =  trello_object.id
  return returnedItem


def print_cards(trello_list_id):
  trello_list = client.get_list(trello_list_id)
  cards = trello_list.list_cards()
  for card in cards:
    print( card.name )

all_boards = client.list_boards()

reinhardt_id    = get_particular_item(all_boards, BOARD)
reinhardt       = client.get_board(reinhardt_id)
reinhardt_lists = reinhardt.all_lists()

for list_to_print in LISTS_TO_PRINT:
    selected_list = get_particular_item(reinhardt_lists, list_to_print)

    print_cards(selected_list)
    print('\n\n')

