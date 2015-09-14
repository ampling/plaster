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


config_dir = os.path.expanduser("~") + '/' + '.config/plaster/'
prefix = config_dir + 'plugins'
config_file = config_dir + 'config'

#
# BEGIN helper funtions 
#

def readin():
    try:
        payload = stdin.read()
    except:
        payload = stdin.buffer.read()
        pass
    return payload

## Use early, use sparingly.
def _read_config():
    '''Parse configuration file, from top to bottom.'''
    config = configparser.ConfigParser()
    config.read(config_file)
    log.info('Configuration file read.')
    return (config)

def null_scan(payload):
    '''Is it binary or not.'''
    try:
        pattern = str("\0\0\0\0")
        if pattern in str(payload):
            binary = False
            log.info('detect: text')
        if pattern not in str(payload):
            binary = True
            log.info('detect: binary')
    except:
        log.error('scan error')
        pass
    return binary

def _relay_command(binary):
    '''Compose a dictionary to compare to each plugins' format.'''
    try:
        if args.type:
             binary = False
             log.info('force image')
        if binary is False:
            command = {'txt': 'yes'}
        if binary is True:
            command = {'img': 'yes'}
    except:
        pass
    try:
        if args.authenticate:
            command.update({'nick': 'yes'})
            log.info('authentication')
        if args.secure:
            command.update({'tls': 'yes'})
            log.info('secure')
        if args.secure:
            command.update({'tls': 'yes'})
            log.info('tls enabled')
        if args.expire:
            command.update({'time': 'yes'})
            log.info('time enabled') 
    except:
        pass
    return command

def _cull_plugin(command, mark): 
    '''Choose the best plugin for the job.'''
    global config
    run = len(config.sections())
    try:
        for mark in range(mark, run):
            plugin_name = config.sections()[mark]
            log.info(plugin_name)
            form = _load_plugin(plugin_name).format()
            diff = set(form.keys()) - set(command.keys())
            sim = set(command.items()) & set(form.items())
            if len(sim) is len(command):
                log.info('pluggin tests OK')
                break
            if len(sim) is not len(command):
                log.info('skipped')
    except:
        log.info('Adapting to connection error.')
        pass
    return (plugin_name, mark)

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
# def passwordeval():
#    gpg

#
# options
#

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--authenticate", 
        help="use authentication set in config", action="store_true")
parser.add_argument("-i", "--input", 
        help="input file", action="store_true")
parser.add_argument("-e", "--expire", 
        help="set paste expiration time", action="store_true")
parser.add_argument("-s", "--secure", 
        help="use secure tls", action="store_true")
parser.add_argument("-t", "--type", 
        help="<text> or <image>", action="store_true")
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
#     pyperclip.copy(link)

#
# main
#

def plaster(payload, command):
    '''Plaster all the things!'''
    global config
    config = _read_config()
    run = len(config.sections())
    attemps = '0'
    mark = 0
    for attemps in range(0, run):
        try:
            cull_ref = _cull_plugin(command, mark)
            plugin_name = cull_ref[0] 
            url = config[plugin_name]['url']
            link = _load_plugin(plugin_name).post(payload, url).rstrip()
            if 'http' in link: # might be better to change to code 200
                break
        except:
            mark = mark + 1
            pass
    return link


def __main__():
    payload = readin() 
    binary = null_scan(payload)
    command = _relay_command(binary)
    link = plaster(payload, command)
    print(link)

def __test__(): 
    log.info('debug mode')
    ###
    #import fileinput

    #for payload in fileinput.input():
    #    link = plaster(payload)
    #    print(link)
    
    payload = readin() 
    binary = null_scan(payload)
    command = _relay_command(binary)
    
    print(command) 
    #link = plaster(payload, command)
    #print(link)



if __name__ == "__main__":
    __main__()
    # __test__()
