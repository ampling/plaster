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
from sys import stdin

prefix = 'plugins'
config_file = 'plaster.conf'
config_dir = os.path.expanduser("~") + 'config/plaster/config'

#
# BEGIN helper funtions 
#

## Use early, use sparingly.
def _read_config():
    '''Parse configuration file, from top to bottom.'''
    config = configparser.ConfigParser()
    config.read(config_file)
    config_ref = config
    print('Configuration file read.') # debug
    return (config_ref)

def _cull_plugin(style): # add: time_to_expire[default=0]
    '''Choose the best plugin for the job.'''
    config_ref = _read_config()
   
    # decision-time
    run = len(config_ref.sections())
    # print(run)
    for n in range(0, run):
        print(n)
        plugin_name = config_ref.sections()[n]
        form = _load_plugin(plugin_name).format()
        if form['txt'] is 'no' and style is True:
            print('Sorry text')
        if form['img'] is 'no' and style is False:
            print('Sorry image')
    
        if (form['txt'] is 'yes' and style is True) or (form['img'] is 'yes' and style is False):
            break
    plugin_url = config_ref[plugin_name]['url']
    return (plugin_name, plugin_url)

def _scout_dir(plugin_name):
    '''Check plugins folder for desired plugin.'''
    list_plugins = glob(prefix + "/"  + "*.py")
    plugin_path = prefix + "/" + plugin_name + ".py" 
    if plugin_path not in list_plugins:
        print('plugin error:', plugin_name, 'not found')
    elif plugin_path in list_plugins:
        found_plugin = plugin_name
        print('scout successful')
        return found_plugin 

def _load_plugin(plugin_name):
    '''Import a dynamic module'''
    plugin_path = prefix + "/"  + plugin_name + ".py"
    spec = SourceFileLoader(plugin_name, plugin_path)
    _plugin = spec.load_module()
    print('plugin', plugin_name, 'loaded') # debug
    return _plugin

def _inspect_form(plugin_name):
    print('temp')

def detect_style(payload):
    '''Test each payload in an attempt to clasify it.
    A simple heuristic based on file(1).
    If characters in payload resemble text return True. 
    If characters in payload resemble binary return False.'''
    txt = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(txt)) 
    style = is_binary_string(payload)
    return style

# add argparser
    # -t = time to expire
    # -s = secure 'use tls'
    # -x = xclip 'send link to clipboard'
    # -v = versose 'debuging'


#
# main
#

def __main__():
    '''Execute funtions in the correct order'''
    payload = stdin.read()
    style = detect_style(payload)
    cull_ref = _cull_plugin(style)
    plugin_name = cull_ref[0] 
    plugin_url = cull_ref[1]
    found_plugin = _scout_dir(plugin_name)
    
    link = _load_plugin(found_plugin).plaster(payload, plugin_url)
    #_inspect_form(plugin_name)
    
    if 'http' in link:
        print(link)

def __test__():
    # payload = stdin.read()
    # form = _load_plugin('sprunge_').format()
    # print(form)
    # _cull_plugin(detect_style(payload))
    _scout_dir("sprunge_")

    #style = detect_style(payload)
    #print(style)

if __name__ == "__main__":
    __main__()
    # __test__()
