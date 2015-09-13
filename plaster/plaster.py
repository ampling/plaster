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

## Use early, use sparingly.
def _read_config():
    '''Parse configuration file, from top to bottom.'''
    config = configparser.ConfigParser()
    config.read(config_file)
    log.info('Configuration file read.')
    return (config)

def detect_binary(payload):
    '''Test each payload in an attempt to clasify it.
    A simple heuristic based on file(1).
    If characters in payload resemble text return True. 
    If characters in payload resemble binary return False.'''
    txt = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
    is_binary_string = lambda bytes: bool(bytes.translate(txt)) 
    binary = is_binary_string(payload)
    return binary

def _relay_command(binary):
    '''define local parameters'''
    try:
        if args.type:
            binary = False
    except:
        pass
    if binary is False:
        command = {'txt': 'yes'}
    if binary is True:
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

def plaster(payload):
    '''Plaster all the things!'''
    binary = detect_binary(payload)
    command = _relay_command(binary)
    global config
    config = _read_config()
    run = len(config.sections()) + 1
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
    payload = stdin.read()
    link = plaster(payload)
    print(link)


def __test__(): 
    log.info('debug mode')
    ###
    #import fileinput

    #for payload in fileinput.input():
    #    link = plaster(payload)
    #    print(link)
    
    binary = True
    payload = stdin.read()
    print(payload)
    link = plaster(payload, binary)
    print(link)



if __name__ == "__main__":
    __main__()
    # __test__()

