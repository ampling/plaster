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
import argparse
import configparser
import logging as log
from glob import glob
from sys import stdin
from importlib.machinery import SourceFileLoader

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
    log.info('Configuration file read.')
    return (config_ref)

def _cull_plugin(style): # add: time_to_expire[default=0]
    '''Choose the best plugin for the job.'''
    config_ref = _read_config()
    run = len(config_ref.sections())
    for mark in range(0, run):
        plugin_name = config_ref.sections()[mark]
        form = _load_plugin(plugin_name).format()
        if (form['txt'] is 'no' and style is True) or (form['img'] is 'no' and style is False):
            print("plugin", plugin_name, "skipped") # debug
            ## exception needed 
        if (form['txt'] is 'yes' and style is True) or (form['img'] is 'yes' and style is False):
            found =  _scout_dir(plugin_name)
            if found is True:
                break
            elif found is False:
                continue

    plugin_url = config_ref[plugin_name]['url']
    return (plugin_name, plugin_url, mark)

def _scout_dir(plugin_name):
    '''Check plugins folder for desired plugin.'''
    list_plugins = glob(prefix + "/"  + "*.py")
    plugin_path = prefix + "/" + plugin_name + ".py" 
    if plugin_path not in list_plugins:
        found = False
        log.error('plugin error:', plugin_name, 'not found')
    elif plugin_path in list_plugins:
        found = True
        log.info('scout successful')
        return found 

def _load_plugin(plugin_name):
    '''Import a dynamic module'''
    plugin_path = prefix + "/"  + plugin_name + ".py"
    spec = SourceFileLoader(plugin_name, plugin_path)
    _plugin = spec.load_module()
    log.info('plugin loaded')
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

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", 
        help="increase output verbosity", action="store_true")
args = parser.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    # log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")

# log.info("This should be verbose.")
# log.warning("This is a warning.")
# log.error("This is an error.")


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
    # found_plugin = _scout_dir(plugin_name)
    
    link = _load_plugin(plugin_name).plaster(payload, plugin_url)
    #_inspect_form(plugin_name)
    
    if 'http' in link: # might be better to change to code 200
        print(link)
    # if http not in link:  # go back to cull
    #     pass mark to cull

def __test__():
    # payload = stdin.read()
    # form = _load_plugin('sprunge_').format()
    # print(form)
    # _cull_plugin(detect_style(payload))
    # style = detect_style(payload)
    # print(style)
    log.info('test')


if __name__ == "__main__":
    __main__()
    # __test__()
