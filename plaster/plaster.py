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
import importlib
from glob import glob # temp

prefix = 'plugins/'
config_dir = path.expanduser("~") + 'config/plaster/config'
config_file = 'plaster.conf'

#
# BEGIN helper funtions
#

#{ Use early, use sparingly.
def read_config(head):
    '''Parse configuration file, from top to bottom.'''
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_file)
    #config.sections()
    plugin = config.sections()[head]
    url = config[plugin]['url']
    #login =
    #passwords =
    return (plugin, url) # add login, password
#{

#{
def cull_plugin(): #add: uptime[default=0]
    '''Choose the best plugin for the job.'''
    plugin = read_config(0)[0] # expand
    url = read_config(0)[1]
    best_plugin = prefix + plugin + ".py"
    return (best_plugin, url)
#}

#{
def scout_plugins(self):
    '''Search plugins folder for desired plugin.'''
    list_plugins = glob("plugins/*.py")
    best_plugin = cull_plugin()[0]
    if best_plugin not in list_plugins:
        print("error: plugin " + best_plugin + " not found") #test me
#}

#{ 
def _load(self):
    filepath = './plugins/'
    module_name = 'sprunge_'
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    plugin = spec.load_module()
    return plugin
#}

#_load('sprunge_')
from plugins import sprunge_ # expand

####

#importlib.util.spec_from_file_location(module_name, filepath)
#importlib.import_module('plugins/sprunge_')

#for n in range(len(config.sections())):
#    plugin = config.sections()[n]
#    print(plugin)

#add argparser

#
# main
#

for payload in fileinput.input():
    plugin = cull_plugin()[0]
    url = cull_plugin()[1]
    scout_plugins(plugin)
    link = sprunge_.posts(payload, url) # expand
    if 'http' in link:
        print(link)
    
