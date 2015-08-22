#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################
""" Plaster

Plaster is a configurable command-line pastebin client.
"""

from plugins import sprunge_
import fileinput
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('plaster.conf')
list = config.sections()
pb = list[0]

for payload in fileinput.input():
    sprunge_.posts(payload)
