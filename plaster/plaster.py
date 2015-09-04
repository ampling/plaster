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
import fileinput
import configparser
from importlib.machinery import SourceFileLoader
from glob import glob

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

def detect_type(ext):
    raster = ['png', 'jpg', 'jpe', 'jpeg', 'giff', 'tiff', 'bmp', 'riff', 
            'exif', 'ppm', 'pgm', 'pbm', 'pnm']
    vector = ['svg','cgm',]
    print(ext)
    if ext in (raster or vector):
        image = 'true'
        return image
    elif ext not in (raster or vector):
        image = 'false'
        return image
#add argparser
    #-t = time to expire
    #-s = secure (use *tls )

#
# main
#

def __main__():
    payload = ''.join(fileinput.input())
    f = readlink('/proc/self/fd/0') #linux only
    ext = f.split('.')[-1]
    print(detect_type(ext))
    cull_ref = _cull_plugin()
    found_plugin = _scout_dir(_cull_plugin()[0])
    plugin_name = cull_ref[0] 
    plugin_url = cull_ref[1]
    link = _load_plugin(found_plugin).push(payload, plugin_url)
    if 'http' in link:
        print(link)


def __test__():
    ext = 'txt'
    print(detect_type(ext))

if __name__ == "__main__":
    __main__()
    #__test__()
