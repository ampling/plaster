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
import io
from os import path
from sys import stdin, stdout
from importlib.machinery import SourceFileLoader

import magic

version = '0.042'

config_dir = path.join(path.expanduser('~'), '.config', 'plaster')
config_file = path.join(config_dir, 'config')
prefix = path.join(config_dir, 'plugins')

#
# options
#

parser = argparse.ArgumentParser(description='plaster v{}'.format(version))
parser.add_argument('infile', default='',
        help='select a file', nargs='?', type=str)
# parser.add_argument("-a", "--authenticate", 
#         help="use authentication set in config", action="store_true")
parser.add_argument("-b", "--binary", nargs='?', default=False, type=bool, 
        help="bypass autodetect; set content as image: True or False")
parser.add_argument("-e", "--expire", nargs='?', default=1, type=int,
        help="time to expire")
parser.add_argument("-s", "--secure", 
        help="use only https", action="store_true")
parser.add_argument("-v", "--verbose", 
        help="increase verbosity", action="count")

# parser.add_argument("-x", "--xclip", 
#         help="send link to clipboard", action="store_true")

args = parser.parse_args()
# if args.xclip:
#     print('xclip')
#     pyperclip.copy(link)

#
# BEGIN helper funtions 
#

def _stdin():
    '''Reads text or binary from stdin.'''
    infile = stdin.buffer.read()
    outfile = open('/tmp/plasti', 'wb')
    outfile.write(infile)
    return (outfile)

def _infile():
    with open(str(args.infile), 'rb') as i, open('/tmp/plasti', 'wb') as out:
        out.write(i.read())
    return '/tmp/plasti'
	
def _incopy():
    pass

def _sniff(infile):
    sniff = str(magic.from_file('/tmp/plasti'))
    return 'image' in sniff

def _config():
    '''Parse configuration file, from top to bottom.'''
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        if config.sections() == []:
            print(config_file, 'appears empty')
            exit(1)
        if args.verbose:
            print('INFO: config:    [PASS]')
        return config
    except Exception as e: 
        print('ERROR: config:')
        print('e:', e)

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
        if args.verbose == 2:
            print('ERROR: command:', e)

def _cull(command, mark): 
    '''Choose the best plugin for the job.'''
    sections = len(config.sections())
    for mark in range(mark, sections):
        try:
            name = config.sections()[mark]
            if args.verbose:
                print(mark + 1, '/', sections, ' >>', name)
            # if args.verbose == 2:
            #     print(mark + 1, '/', sections)
            form = _load(name).formula()
            ## here 
        except Exception as e:
            name = 'null'
            if args.verbose:
                print('WARNING: cull   ', '[FAIL]')
            if args.verbose == 2:
                print('e:', e)
            continue
        try:  
            diff = set(form.keys()) - set(command.keys())
            sim = set(command.items()) & set(form.items())
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
        # errors here
        module = spec.load_module()
        if args.verbose == 2:
            print('INFO:', 'load      ', '[PASS]')
        return module
    except Exception as e:
        if args.verbose == 2:
            print('e:', e)

def paste(name, url, data):
    '''
    Sends data to specified pastebin.
    example: paste('clbin', 'https://clbin.com', 'Hello, World!')
    The return value is a dicionary {'link': 'https://clbin.com'}
    '''
    try:
        # url = config[name]['url']
        response = _load(name).post(url, data)
        if args.verbose == 2:
            print('INFO:','paste     ', '[PASS]')
        return response
    except Exception as e:
        if args.verbose:
            print('WARNING: paste   [FAIL]')
        if args.verbose == 2:
            print('e:', e)


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
            url = config[name]['url']
            response = paste(name, url, data)
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

# add passwordeval
# def passwordeval():
#    gpg

#
# main
#

config = _config()

def __main__():
    if args.infile:
        entry = _infile()
        if args.verbose:
            print('infile mode [ON]')
    ##_xcopyin
    if not args.infile:  # or _xcopyin
        entry = _stdin()
    binary = _sniff('/tmp/plasti')
    command = _command(binary)
    try:
        '''sends hyperlink to stdout'''
        if binary is False:
            with open('/tmp/plasti', 'r') as f:
                read_data = f.read()
        if binary is True:
            with open('/tmp/plasti', 'rb') as f:
                data = f.read()
        print('f =', f)    
        print('data =', read_data)
        response = plaster(command, read_data)
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
            # notify of a bad connection.
            #if  str(response['reason']) 
            #    reason = str(response['reason'])
            #if 'Connection' in reason:
            #    if args.verbose:
            #        print('ERROR:', 'connection problem')
        except:
            pass
        #else:
        #    if args.verbose:
        #        print('ERROR:', 'main ', '   [FAIL]')
        #    if not args.verbose:
        #        print('to debug, try plaster -v')
    except Exception as e:
        if args.verbose == 2:
            print("ERROR: main:", e)
        raise
    
def __test__(): 
    print('debug mode [ON]')
    ###
    try:
        '''send link to stdout'''
        
        
        with open('/tmp/plasti', 'r') as f:
            read_data = f.read()
        
        print(read_data)
    except Exception as e:
        raise
        print('ERROR: test:', e)
    
    
if __name__ == "__main__":
    __main__()
    # __test__()
