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

def is_binary(payload):
    '''Is it binary or not.'''
    try:
        pattern = bool("\0\0\0\0")
        for pattern in payload:
            binary = False
            log.info('detect: text')
            break
        if pattern not in payload:
            binary = True
            log.info('detect: binary')
    except:
        log.error('unable to scan paste')
        pass
    return binary

def _get_command(binary):
    '''Compose a dictionary to compare to each plugins' format.'''
    try:
        # if args.type:
        #      binary = False
        #      log.info('force image')
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

def _cull(command, mark): 
    '''Choose the best plugin for the job.'''
    global config
    log.info('start cull')
    sections = len(config.sections())
    #if mark is not 0:
    #    mark = mark + 1
    try:
        for mark in range(mark, sections):
            # name of plugin
            name = config.sections()[mark]
            log.info(name)
            match = _fnmatch(name)
            if match is False:
                log.info('adapting to match error')
            if match is True:
                form = _load(name).format()
                diff = set(form.keys()) - set(command.keys())
                sim = set(command.items()) & set(form.items())
                if len(sim) is len(command):
                    log.info('plugin checks out')
                    break
                if len(sim) is not len(command):
                    log.info('skipped')
    except:
        log.info('adapting...')
        pass
    log.info('leave cull')
    return (name, mark)

def _fnmatch(name):
    '''Check whether the plugins folder matches the desired plugin.'''
    list_plugins = glob(prefix + "/"  + "*.py")
    plugin_path = prefix + "/" + name + ".py" 
    if plugin_path in list_plugins:
        match = True
        log.info('plugin path confirmed')
    else:
        match = False
        print('problem matching plugin', name)
    return match 

def _load(name):
    '''Import a module by name.'''
    try:
        plugin_path = prefix + "/"  + name + ".py"
        spec = SourceFileLoader(name, plugin_path)
        module = spec.load_module()
        return module
    except:
        print('problem loading plugin', name)

def _ping():
    
    return netstatus

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
    sections = len(config.sections())
    attemps = '0'
    mark = 0
    for attemps in range(0, sections):
        '''compensating for lame servers'''
        try:
            cull = _cull(command, mark)
            mark = mark + 1 
            name = cull[0]
            url = config[name]['url']
            link = _load(name).post(payload, url).rstrip()
            log.info('loading plugin...')
            if 'http' in link: # might be better to change to code 200
                break
            else:
                log.info('another one bites the dust')
        except:
            log.info('plaster adapting...')
            mark = mark + 1
            pass
    return link

def __main__():
    payload = readin() 
    binary = is_binary(payload)
    command = _get_command(binary)
    try:
        '''send link to stdout'''
        print(plaster(payload, command))
    except:
        log.error('unable to plaster')
        raise
    

def __test__(): 
    log.info('debug mode')
    ###
    payload = readin() 
    binary = is_binary(payload)
    command = _get_command(binary)
    print(command) 

if __name__ == "__main__":
    __main__()
    # __test__()
