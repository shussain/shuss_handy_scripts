#!/usr/bin/python

"""
    This script parses Empathy chat logs (in XML) and outputs
    human readable text.

    ./parse_chatlog.py [filename]

    NOTE: Location of Empathy logs is at: $HOME/.local/share/TpLogger/logs

    OUTPUT:
        (20151127T22:38:10) Shahid Afridi: Ready for some cricket?
        (20151127T23:36:50) Inzimam Al-Haq: No. Having dinner.

"""
import sys, os
from xml.dom import minidom

USAGE = './parse_chatlog.py filename'
if len(sys.argv) != 2:
    print "Following the following usage:"
    print "\t" + USAGE
    sys.exit(1)

filename=sys.argv[1]

if not os.path.isfile(filename):
    print "File: {} does not exist".format(filename)
    sys.exit(1)

xmldoc = minidom.parse(filename)
messages = xmldoc.getElementsByTagName('message')

for message in messages:
    ind_message =  '(' + message.attributes['time'].value + ') '
    ind_message += message.attributes['name'].value + ': '
    ind_message += message.childNodes[0].nodeValue
    print ind_message

