#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) [2015-08-06], ISC license, [Ampling <plaster@ampling.com>]
#
'''
 ____  __      __    ___  ____  ____  ____ 
(  _ \(  )    /__\  / __)(_  _)( ___)(  _ \
 )___/ )(__  /(__)\ \__ \  )(   )__)  )   /
(__)  (____)(__)(__)(___/ (__) (____)(_)\_)

Plaster is an adaptable command-line pastebin client.
'''

import argparse
import configparser
from os import path
from glob import glob
from sys import stdin
from importlib.machinery import SourceFileLoader

config_dir = path.join(path.expanduser('~'), '.config', 'plaster')
config_file = path.join(config_dir, 'config')
prefix = path.join(config_dir, 'plugins')

#
# options
#

parser = argparse.ArgumentParser()
# parser.add_argument("-a", "--authenticate", 
#         help="use authentication set in config", action="store_true")
parser.add_argument("-i", "--input", 
        help="input file")
parser.add_argument("-e", "--expire", 
        help="set paste expiration time")
parser.add_argument("-s", "--secure", 
        help="use secure tls", action="store_true")
parser.add_argument("-t", "--type", 
        help="<text> or <image>")
parser.add_argument("-v", "--verbose", 
        help="explain what is being done", action="store_true")
# parser.add_argument("-x", "--xclip", 
#         help="send link to clipboard", action="store_true")

args = parser.parse_args()

# if args.xclip:
#     print('xclip')
#     pyperclip.copy(link)

#
# BEGIN helper funtions 
#

def _readin():
    '''Reads text or binary from stdin.'''
    try:
        payload = stdin.read()
        binary = False
        if args.verbose:
            print('Autodetect:    [text]')
    except KeyboardInterrupt:
        print('try:', 'plaster < example.txt' )
        exit(1)
    except Exception as e:
        payload = stdin.buffer.read()
        binary = True
        if args.verbose:
            print('INFO:', 'type:    [binary]')
    return (payload, binary)

## Use early, use sparingly.

def _config():
    '''Parse configuration file, from top to bottom.'''
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        if args.verbose:
            print('INFO: config:  [OK]')
        return config
    except Exception as e: 
        print('ERROR: config:', e)
        raise


def _command(binary):
    '''Compose a dictionary to compare to each plugins' formula.'''
    try:
        if args.type:
            binary = False
            if args.verbose:
                print('text mode [ON]')
        if binary is False:
            command = {'txt': 'yes'}
        if binary is True:
            command = {'img': 'yes'}
    except:
        pass
    try:
        # if args.authenticate:
        #     command.update({'nick': 'yes'})
        #     if args.verbose:
        #         print('authentication mode enabled')
        if args.secure:
            command.update({'tls': 'yes'})
            if args.verbose:
                print('tls mode enabled')
        # if args.expire:
        #     command.update({'time': 'yes'})
        #     if args.verbose:
        #         print('ephemeral mode enabled') 
        return command
    except Exception as e:
        if args.verbose:
            print('ERROR: command:', e)

def _cull(command, mark): 
    '''Choose the best plugin for the job.'''
    sections = len(config.sections())
    for mark in range(mark, sections):
        try:
            # name of plugin
            name = config.sections()[mark]
            if args.verbose:
                print('>>>', name)
            match = _fnmatch(name)
            if match is False:
                if args.verbose:
                    print('*cull continues*')
            if match is True:
                form = _load(name).formula()
                diff = set(form.keys()) - set(command.keys())
                sim = set(command.items()) & set(form.items())
                if len(sim) is len(command):
                    if args.verbose:
                        print('INFO:', 'cull     [OK]')
                    break
                if len(sim) is not len(command):
                    if args.verbose:
                        print('INFO:', 'skipped')
                    name = None
        except Exception as e:
            if args.verbose:
                print('ERROR: cull:', e)
    return (name, mark)

def _fnmatch(name):
    '''Check whether the plugins folder matches the desired plugin.'''
    list_plugins = glob(prefix + '/' + '*.py') # fix
    plugin_path = path.join(prefix, '.'.join([name, 'py']))
    if plugin_path in list_plugins:
        match = True
        if args.verbose:
            print('INFO:', 'fnmatch  [OK]')
    else:
        match = False
        if args.verbose:
            print('WARNING: unable to match plugin:', name)
            # print(str('  try: ls'), prefix + "/")
    return match 

def _load(name):
    '''Import a module by name.'''
    try:
        plugin_path = path.join(prefix, '.'.join([name, 'py']))
        spec = SourceFileLoader(name, plugin_path)
        module = spec.load_module()
        if args.verbose:
            print('INFO:', 'load     [OK]')
        return module
    except Exception as e:
        print('problem loading plugin', name)
        if args.verbose:
            print('ERROR: load:', e)

def paste(name, payload):
    '''send to bin'''
    try:
        url = config[name]['url']
        response = _load(name).post(payload, url)
        return response
    except Exception as e:
        if args.verbose:
            print('WARNING: paste:', e)


def plaster(command, payload):
    '''Adapt to all the things!'''
    sections = (len(config.sections()))
    i, mark = 0, 0  
    for i in range(sections):
        '''compensating for downtime'''
        try:
            if mark > sections:
                if args.verbose:
                    print('exit: mark')
                exit(1)
            cull = _cull(command, mark)
            name = cull[0]
            if name == None:
                if args.verbose:
                    print('exit: name')
                exit(1)
            mark = mark + 1
            response = paste(name, payload)
            try:
                reason = str(response['reason'])
                link = str(response['link'])
                code = str(response['code'])
            except Exception as e:
                if args.verbose:
                    print('WARNING:', 'plugin:', e) 
                continue
            if '200' in code: 
                break
            elif code is None:
                if args.verbose:
                    print('INFO:', code)
        except Exception as e:
            if args.verbose:
                print('WARNING: plaster:', e)
                print('*Plaster adapts*')
            mark = mark + 1
            # finds another
    return response

# add passwordeval
# def passwordeval():
#    gpg

#
# main
#

config = _config()

def __main__():
    payload = _readin() 
    binary = payload[1]
    command = _command(binary)
    try:
        '''send hyperlink to stdout'''
        response = plaster(command, payload[0])
        if response is not None:
            reason = str(response['reason'])
            link = str(response['link'])
            code = str(response['code'])
            if 'Connection' in reason:
                if args.verbose:
                    print('ERROR:', 'connection problem')
            elif 'http' in link:
                print(str(link))
            else:
                if args.verbose:
                    print('INFO:', 'unable to plaster')
                if not args.verbose:
                    print('to debug, try plaster -v')
        else:
            if args.verbose:
                print('please fix plugin:')
    except Exception as e:
        if args.verbose:
            print("ERROR _main:", e)
    
def __test__(): 
    print('debug mode [ON]')
    ###
    payload = 'test'
    binary = False
    command = _command(binary)
    print(config)
    try:
        '''send link to stdout'''
        _load('sprunge_requests').formula()
        #name = 'sprunge_requests'
        #response  = paste(name, payload)
        #reason = str(response['reason'])
        #print(response['link'])
        #if 'Connection' in reason: print('connection error')
    except Exception as e:
        print('ERROR: text:', e)

if __name__ == "__main__":
    __main__()
    ## __test__()
