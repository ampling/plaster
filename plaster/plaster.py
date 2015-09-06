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

import os
import configparser
from importlib.machinery import SourceFileLoader
from glob import glob
import sys


prefix = 'plugins'
config_file = 'plaster.conf'
config_dir = os.path.expanduser("~") + 'config/plaster/config'

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

def _cull_plugin(): # add: time_to_expire[default=0]
    '''Choose the best plugin for the job.'''
    # if config_ref doesn't exist
    config_ref = _read_config()
    # decision-time
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

def detect_raster(subject):
    textchars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - 
            {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(None, textchars)) 
    cat = is_binary_string(subject)
    print(cat)



#add argparser
    # -t = time to expire
    # -s = secure (use *tls )

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
    # subject = os.open(''.join(stdin.readline()), "rb", buffering=0)
    # subject = ''.join(stdin.readline())
    BINARY=True
    istream = sys.stdin
    global subject
    subject = istream.read()
    print("len="+str(len(subject)))
    detect_raster(subject)


if __name__ == "__main__":
    #__main__()
    __test__()
