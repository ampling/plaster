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
from glob import glob
import fileinput
import configparser


config = configparser.ConfigParser()
config.sections()
config.read('plaster.conf')




def look():
    '''look in plugin filder'''
    plugins = glob("plugins/*")
    print(plugins[3])

#for payload in fileinput.input():
#    sprunge_.posts(payload)


look()
