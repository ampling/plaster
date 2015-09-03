#! /usr/bin/env python3
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################
'''
PLASTER

Plaster is a configurable command-line pastebin client.
'''

from os import path
import fileinput
import configparser
from importlib.machinery import SourceFileLoader
from glob import glob

prefix = 'plugins/'
config_dir = path.expanduser("~") + 'config/plaster/config'
config_file = 'plaster.conf'
plugin_dir = 'plugins/'

#
# BEGIN helper funtions 
#

#{ Use early, use sparingly.
def _read_config():
    '''Parse configuration file, from top to bottom.'''
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_file)
    config.sections()
    config_ref = config
    return (config_ref)
#}

def _cull_plugin(): #add: uptime[default=0]
    '''Choose the best plugin for the job.'''
    #if config_ref doesn't exist
    config_ref = _read_config()
    #decision-time
    n = 0 #test
    plugin_name = config_ref.sections()[n]
    plugin_url = config_ref[plugin_name]['url']
    return (plugin_name, plugin_url)

def _scout_plugins(plugin_name):
    '''Search plugins folder for desired plugin.'''
    expression = plugin_dir + "*.py"
    list_plugins = glob(expression)
    plugin_path = prefix + str(plugin_name) + ".py" 
    if plugin_path not in list_plugins:
        print("error: plugin " + "<name>" + " not found")
    elif plugin_path in list_plugins:
        print("Plugin found")
        found_plugin = plugin_name
    return found_plugin 

def _load_plugin(plugin_name):
    plugin_path = prefix + str(plugin_name) + ".py"
    spec = SourceFileLoader(plugin_name, plugin_path)
    _plugin = spec.load_module()
    return _plugin

#add argparser

#
# main
#

def __main__():
    payload = ''.join(fileinput.input())
    cull_ref = _cull_plugin()
    found_plugin = _scout_plugins(_cull_plugin()[0])
    plugin_name = cull_ref[0] 
    plugin_url = cull_ref[1]
    link = _load_plugin(found_plugin).posts(payload, plugin_url)
    if 'http' in link:
        print(link)


if __name__ == "__main__":
    #__test__()
    __main__()


#def __test__():
