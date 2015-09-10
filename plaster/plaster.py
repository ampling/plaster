#! /usr/bin/env python3
##############################################################################
#
# Copyright (c) [2015-08-06], ISC license, [Ampling <plaster@ampling.com>]
#
##############################################################################
'''
 ____  __      __    ___  ____  ____  ____ 
(  _ \(  )    /__\  / __)(_  _)( ___)(  _ \
 )___/ )(__  /(__)\ \__ \  )(   )__)  )   /
(__)  (____)(__)(__)(___/ (__) (____)(_)\_)

Plaster is an adaptable command-line pastebin client.
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

def detect_style(payload):
    '''Test each payload in an attempt to clasify it.
    A simple heuristic based on file(1).
    If characters in payload resemble text return True. 
    If characters in payload resemble binary return False.'''
    txt = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(txt)) 
    style = is_binary_string(payload)
    return style

def _relay_command(style):
    '''define local parameters'''
    if style is True:
        command = {'txt': 'yes'}
    if style is False:
        command = {'img': 'yes'}
    try:
        if args.login:
            command.update({'nick': 'yes'})
            log.info('login')
        if args.secure:
            command.update({'tls': 'yes'})
            log.info('secure')
        if args.secure:
            command.update({'tls': 'yes'})
            log.info('secure')
        if args.time:
            command.update({'time': 'yes'})
            log.info('time') 
    except:
        pass
    return command

def _cull_plugin(command): # add (run, mark) 
    '''Choose the best plugin for the job.'''
    config_ref = _read_config()
    run = len(config_ref.sections())
    try:
        for mark in range (0, run):
            plugin_name = config_ref.sections()[mark]
            form = _load_plugin(plugin_name).format()
            diff = set(form.keys()) - set(command.keys())
            sim = set(command.items()) & set(form.items())
            if len(sim) is len(command):
                log.info('pluggin tests OK')
                break
            if len(sim) is not len(command):
                log.info('skipped')

    except:
        pass
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



# add passwordeval
#def passwordeval():
#    gpg

#
# options
#

parser = argparse.ArgumentParser()
# parser.add_argument("-l", "--login", 
#         help="read login", action="store_true")
# parser.add_argument("-s", "--secure", 
#         help="secure tls", action="store_true")
# parser.add_argument("-t", "--time", 
#         help="time to expire", action="store_true")
parser.add_argument("-v", "--verbose", 
        help="increase output verbosity", action="store_true")
# parser.add_argument("-x", "--xclip", 
#         help="send link to clipboard", action="store_true")

args = parser.parse_args()
if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")

# log.info("This should be verbose.")
# log.warning("This is a warning.")
# log.error("This is an error.")

# if args.xclip:
#     print('xclip')


#
# main
#

def __main__():
    '''Plaster all the things!'''
    payload = stdin.read()
    style = detect_style(payload)
    command = _relay_command(style)
    cull_ref = _cull_plugin(command)
    plugin_name = cull_ref[0] 
    plugin_url = cull_ref[1]
    link = _load_plugin(plugin_name).plaster(payload, plugin_url)
     
    if 'http' in link: # might be better to change to code 200
        print(link)
    
    # if http not in link:  # go back to cull
    #     pass mark to cull

def __test__(): 
    log.info('test')
    ###

    #payload = stdin.read()
    #style = detect_style(payload)
    command = _relay_command(True)
    best = _cull_plugin(command) 
    print(best)




if __name__ == "__main__":
     __main__()
    #__test__()
