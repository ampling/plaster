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
from importlib.machinery import SourceFileLoader
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
    path = prefix + plugin + ".py"
    return (path, url)
#}

#{
def scout_plugins(self):
    '''Search plugins folder for desired plugin.'''
    list_plugins = glob("plugins/*.py")
    path = cull_plugin()[0]
    if path not in list_plugins:
        print("error: plugin " + path + " not found") #test me
    return path
#}

#{   
def _load(plugin, path):
    scout_plugins(plugin)
    spec = SourceFileLoader(plugin, path)
    _plugin = spec.load_module()
    return _plugin
#}


#from plugins import sprunge_ # expand
#importlib.util.spec_from_file_location(module_name, filepath)
#importlib.import_module('plugins/sprunge_')

#add argparser

#
# main
#

for payload in fileinput.input():
    path = './plugins/sprunge_.py'
    plugin = cull_plugin()[0]
    url = cull_plugin()[1]
    link = _load(plugin, path).posts(payload, url) # expand
    if 'http' in link:
        print(link)
    
