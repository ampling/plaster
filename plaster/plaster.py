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

from os import path, readlink
import configparser
from importlib.machinery import SourceFileLoader
from glob import glob
from sys import stdin

import magic

prefix = 'plugins'
config_file = 'plaster.conf'
config_dir = path.expanduser("~") + 'config/plaster/config'

#
# BEGIN helper funtions 
#

#{ Use early, use sparingly.
def _read_config():
    '''Parse configuration file, from top to bottom.'''
    config = configparser.ConfigParser()
    config.read(config_file)
    config_ref = config
    return (config_ref)
#}

def _cull_plugin(): #add: time_to_expire[default=0]
    '''Choose the best plugin for the job.'''
    #if config_ref doesn't exist
    config_ref = _read_config()
    #decision-time
    n = 0 #debug
    plugin_name = config_ref.sections()[n]
    plugin_url = config_ref[plugin_name]['url']
    return (plugin_name, plugin_url)

def _scout_dir(plugin_name):
    '''Search plugins folder for desired plugin.'''
    list_plugins = glob(prefix + "/"  + "*.py")
    plugin_path = prefix + "/" + plugin_name + ".py" 
    if plugin_path not in list_plugins:
        print("error: plugin " + "<name>" + " not found")
    elif plugin_path in list_plugins:
        print("Plugin found")
        found_plugin = plugin_name
    return found_plugin 

def _load_plugin(plugin_name):
    plugin_path = prefix + "/"  + plugin_name + ".py"
    spec = SourceFileLoader(plugin_name, plugin_path)
    _plugin = spec.load_module()
    return _plugin

#def detect_type(ext):
    

#add argparser
    #-t = time to expire
    #-s = secure (use *tls )
    #-f = file

#
# main
#

def __main__():
    payload = ''.join(stdin.readline())
    
    cull_ref = _cull_plugin()
    found_plugin = _scout_dir(_cull_plugin()[0])
    plugin_name = cull_ref[0] 
    plugin_url = cull_ref[1]
    link = _load_plugin(found_plugin).push(payload, plugin_url)
    if 'http' in link:
        print(link)


def __test__():
    f = stdin()
    print(magic.from_buffer(open(f)))


if __name__ == "__main__":
    __main__()
    #__test__()
