#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################
""" Plaster

Plaster is a configurable command-line pastebin client.
"""

from os import path
import fileinput
import configparser
from glob import glob

prefix = 'plugins/'
config_dir = path.expanduser("~") + 'config/plaster/config'

#
# BEGIN helper funtions
#

def get_config(head):
    '''Check configuration file, from top to bottom.'''
    config = configparser.ConfigParser()
    config.sections()
    config.read('plaster.conf')
    #config.sections()
    plugin = config.sections()[head]
    url = config[plugin]['url']
    return (plugin, url)

def cull_plugin():
    '''Chooses the best plugin for the job.'''
    plugin = get_config(0)[0]
    url = get_config(0)[1]
    best_plugin = prefix + plugin + ".py"
    return (best_plugin, url)

def scout_plugins(self):
    '''Search plugins folder for desired plugin.'''
    list_plugins = glob("plugins/*.py")
    best_plugin = cull_plugin()[0]
    if best_plugin not in list_plugins:
        print("error: plugin not found")

from plugins import sprunge_ #fix needed

#for n in range(len(config.sections())):
#    plugin = config.sections()[n]
#    print(plugin)
   

#
# main
#

for payload in fileinput.input():
    plugin = cull_plugin()[0]
    url = cull_plugin()[1]
    scout_plugins(plugin)
    sprunge_.posts(payload, url)

