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
import mimetypes
import itertools
import random
import tempfile
from sys import stdin
from os import path, isatty, stat
from importlib.machinery import SourceFileLoader

try:
    import magic
    import_magic = True
except Exception as e:
    import_magic = False
    print('e:', e)

try:
    import pyperclip
    import_pyperclip = True
except Exception as e:
    import_pyperclip = False
    print('e:', e)

version = '0.0.6'

config_dir = path.join(path.expanduser('~'), '.config', 'plaster')
config_file = path.join(config_dir, 'config')
prefix = path.join(config_dir, 'plugins')

#
# options
#

parser = argparse.ArgumentParser(description='plaster v{}'.format(version))
parser.add_argument('content', default='',
        help='select a file', nargs='?', type=str)
parser.add_argument('-b', '--binary', nargs='?', default=False, type=bool, 
        help='bypass autodetect; set content as image: True or False')
parser.add_argument('-e', '--expiry', nargs='?', default=0, type=int,
        help='expiry time in days')
parser.add_argument('-f', '--force', 
        help='force unsafe behavior', action='store_true')
parser.add_argument('-l', '--login', 
        help='authentication set in config', action='store_true')
parser.add_argument('-s', '--secure', 
        help='https everywhere', action='store_true')
parser.add_argument('-v', '--verbose', 
        help='increase verbosity', action='count')
parser.add_argument('-x', '--xclip', 
        help='copy link to clipboard', action='store_true')
parser.add_argument('-X', '--Xclip', 
        help='publish your clipboard; requires --force', action='store_true')
args = parser.parse_args()

#
# BEGIN helper functions 
#

def _inlet():
    '''Reads all, returns file location'''
    try:
        ## known path
        if args.content:
            content_path = args.content
        elif args.Xclip and not args.force:
            print('plaster your clipboard for all to see?')
            print('add -f')
            exit(1)
        elif args.Xclip and args.force: 
            content = bytes(pyperclip.paste(), 'utf-8')
            content_path = None
        elif isatty(0):
            print('enter a file to plaster')
            content_path = input('$ ')
        else: 
            content_path = None
            content = stdin.buffer.read()
        if content_path is not None:
            with open(str(content_path), 'rb') as i:
                content = i.read()
        return content
    except KeyboardInterrupt:
        print()
        exit('for help, try: plaster -h')
    except Exception as e:
        print('e: inlet:', e)
        exit(1)

def _sniff(content):
    if import_magic == True:
        sniff = (magic.from_buffer(content)).decode('utf-8')
    return 'image' in sniff

def _config():
    '''Parse configuration file, from top to bottom.'''
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        if stat(config_file).st_size == 0:
            print('e: config appears empty, exiting')
            exit(config_file)
        if config.sections() == []:
            print('e: config needs sections, exiting')
            print(config_file)
            exit(1)
        if args.verbose:
            print('INFO: config:    [PASS]')
        return config
    except Exception as e: 
        print('ERROR: config    [FAIL]')
        print('e:', e)
        exit(1)

def _command(binary):
    '''Compose a dictionary to match specified parameters.'''
    try:
        if binary is False:
            command = {'txt': 'yes'}
        if binary is True:
            command = {'img': 'yes'}
    except:
        pass
    try:
        if args.login:
            command.update({'login': 'yes'})
            if args.verbose:
                print('authentication mode enabled')
        if args.secure:
            command.update({'tls': 'yes'})
            if args.verbose:
                print('tls mode enabled')
        if args.expiry:
            command.update({'time': 'yes'})
            if args.verbose:
                print('ephemeral mode enabled') 
        return command
    except Exception as e:
        if args.verbose == 2:
            print('ERROR: command:', e)

def _cull(command, mark): 
    '''Choose the best plugin for the job.'''
    sections = len(config.sections())
    for mark in range(mark, sections):
        try:
            name = config.sections()[mark]
            if args.verbose:
                print(mark + 1, '/', sections, ' >>>', name)
            formula = _load(name).tell_form()
        except Exception as e:
            name = 'null'
            if args.verbose:
                print('WARNING: cull   ', '[FAIL]')
            if args.verbose == 2:
                print('e:', e)
            continue
        try:  
            diff = set(formula.keys()) - set(command.keys())
            sim = set(command.items()) & set(formula.items())
            if len(sim) is len(command):
                if args.verbose:
                    print('INFO:', 'cull      ', '[PASS]')
                break
            if len(sim) is not len(command):
                if args.verbose:
                    print('INFO:', 'cull      ', '[FAIL]')
                name = None
                continue
        except Exception as e:
            if args.verbose == 2:
                print('ERROR: cull:', e)
    return (name, mark)

def _load(name):
    '''Import a module by name.'''
    try:
        plugin_path = path.join(prefix, '.'.join([name, 'py']))
        spec = SourceFileLoader(name, plugin_path)
        module = spec.load_module()
        if args.verbose == 2:
            print('INFO:', 'load      ', '[PASS]')
        return module
    except Exception as e:
        if args.verbose == 2:
            print('e:', e)

def push(name, data):
    '''
    Sends data to specified pastebin.
    example: push('clbin', 'https://clbin.com', 'Hello, World!')
    The return value is a dicionary {'link': 'https://clbin.com'}
    '''
    try:
        if args.login:
            login = (config[name]['username'], config[name]['password'])
        else:
            login = (None, None)
        request_chain = {
                'url': config[name]['url'], 
                'data': data, 
                'time': args.expiry, 
                'login': login
                }
        response = 'null'
        response = _load(name).tell_post(request_chain)
        if 'http' not in str(response['link']):
            if response['reason']:
                if args.verbose:
                    print('ERROR: plugin    [FAIL]')
                if args.verbose == 2:
                    print('e:', response['reason'])
        else:
            if args.verbose == 2:
                print('INFO:','push      ', '[PASS]')
    except Exception as e:
        if args.verbose:
            print('WARNING: push    [FAIL]')
        if args.verbose == 2:
            print('e:', e)
    finally: 
        return response

def plaster(command, data):
    '''
    Compensates for ineffective pastebins.
    example: plaster({'txt': 'yes'}, "Hello, World!") 
    The return value is a dicionary {'link': 'https://clbin.com'}
    '''
    sections = (len(config.sections()))
    i, mark = 0, 0
    response = 'null'
    for i in range(0, sections):
        ## i & mark should work in unison.
        try:
            cull = _cull(command, mark)
            name = cull[0]
            mark = cull[1] + 1
            i = cull[1] + 1
            # url = config[name]['url']
            response = push(name, data)
            try:
                link = str(response['link'])
            except Exception as e:
                if args.verbose:
                    print('WARNING: plugin  [FAIL]')
                if args.verbose == 2:
                    print('e:', e) 
                continue
            if 'http' in link: 
                break
            if mark <= sections:
                if args.verbose == 2:
                    print('####')
            '''plaster finds another plugin'''
        except Exception as e:
            response = 'null'
            mark = mark + 1
            i = i + 1
            if args.verbose:
                print('WARNING: plaster [FAIL]')
            if args.verbose == 2:
                print('e:', e)
            continue
    return response

#
# main
#

config = _config()

def __main__():
    content = _inlet()
    binary = _sniff(content)
    command = _command(binary)
    try:
        '''sends hyperlink to stdout'''
        response = plaster(command, content)
        if response is 'null':
            if args.verbose:
                print('done')
            exit(1)
        link = 'null'
        link = str(response['link'])
        try:
            if link != 'null' and 'http' in link:
                if args.verbose == 2:
                    print('INFO: main       [PASS]')
                print(str(link).rstrip())
        except:
            if args.verbose:
               print('ERROR:', 'main ', '   [FAIL]')
            if not args.verbose:
               print('to debug, try plaster -v')
            
        ## optional clipboard feature
        if args.xclip:
            pyperclip.copy(link)
    except Exception as e:
        if args.verbose == 2:
            print('ERROR: main:', e)
        raise
		
def __test__(): 
    print('debug mode [ON]')
    ###
    try:
        '''send link to stdout'''
    except Exception as e:
        raise
        print('ERROR: test:', e)
    
if __name__ == '__main__':
    __main__()
    # __test__()
