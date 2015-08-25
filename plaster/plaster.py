#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
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



for payload in fileinput.input():
    if 
    sprunge_.posts(payload)
