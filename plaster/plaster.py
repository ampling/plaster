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
from os import path
from sys import stdin
from importlib.machinery import SourceFileLoader

config_dir = path.join(path.expanduser('~'), '.config', 'plaster')
config_file = path.join(config_dir, 'config')
prefix = path.join(config_dir, 'plugins')

#
# options
#

parser = argparse.ArgumentParser()
parser.add_argument('infile', default='',
        help='infile', nargs='?', type=str)
# parser.add_argument("-a", "--authenticate", 
#         help="use authentication set in config", action="store_true")
parser.add_argument("-b", "--binary", 
        help="set to True or False")
parser.add_argument("-e", "--expire", 
        help="set paste expiration time")
parser.add_argument("-s", "--secure", 
        help="use secure tls", action="store_true")
parser.add_argument("-v", "--verbose", 
        help="explain what is being done", action="count")

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
    try:
        data = stdin.read()
        binary = False
        if args.verbose:
            print('+text detected')
    except KeyboardInterrupt:
        print('try:', 'plaster < example.txt' )
        exit(1)
    except Exception as e:
        data = stdin.buffer.read()
        binary = True
        if args.verbose:
            print('+binary detected')
    return (data, binary)

def _infile():
    buffersize = 200000 # change to var
    infile = open(str(args.infile), 'rb')
    outfile = open('/tmp/plastered', 'wb')
    buffer = infile.read(buffersize)
    while len(buffer):
        outfile.write(buffer)
        # print('.', end='')
        buffer = infile.read(buffersize)
    brick = str('/tmp/plastered')
    return brick

def _incopy():
    pass

def _guess(infile):
    guess = mimetypes.guess_type(str(infile))
    print(infile)
    if 'text/plain' in guess:
        print('text')
        binary = False
    elif 'image/png' in guess:
        print('image')
        binary = True
    else:
        print('unknown type =', guess)
        print(guess)
        binary = None
    return binary

## Use early, use sparingly.

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
        if args.verbose:
            print('ERROR: config:', e)

def _command(binary):
    '''Compose a dictionary to compare to each plugins' formula.'''
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
                print('>>', name)
            if args.verbose == 2:
                print(mark + 1, '/', sections)
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
    '''send to bin'''
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
    '''Adapt to all the things!'''
    sections = (len(config.sections()) - 1)
    i, mark = 1, 0
    for i in range(1, sections):
        '''compensating for downtime'''
        try:
            # if args.verbose == 2:
            #     print('p:', mark + 1,'/',sections)
            ### action
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
                if args.verbose:
                    print('>', end='')
        except Exception as e:
            response = 'null'
            if args.verbose:
                print('WARNING: plaster [FAIL]')
            if args.verbose == 2:
                print('e:', e)
            mark = mark + 1
            i = i + 1
            '''plaster finds another plugin'''
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
        data = _infile()
        if args.verbose:
            print('infile mode [ON]')
    ##_xcopyin
    if not args.infile:  # or _xcopyin
        sdata = _stdin()
        binary = sdata[1]
        data = sdata[0]
    if not args.binary:
        # binary = _guess(infile)
        pass
    binary = args.binary == 'True'
    command = _command(binary)
    try:
        '''sends hyperlink to stdout'''
        response = 'null'
        # data = args.infile
        response = plaster(command, data)
        if response is 'null':
            if args.verbose:
                print('done')
            exit(1)
        link = 'null'
        link = str(response['link'])
        
        try:
            if args.verbose == 2:
                print('INFO: main       [PASS]')
            if link != 'null' and 'http' in link:
                print(str(link).rstrip())
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
        name = 'ptpb_requests'
        url = 'https://ptpb.pw'
        payload = _infile()
        print(payload)
        response  = paste(name, url, payload)
        print(response)
        # print('link =', response['link'])
        # if 'Connection' in reason: print('connection error')
    
    except Exception as e:
        raise
        print('ERROR: test:', e)
    
    
if __name__ == "__main__":
    __main__()
    # __test__()
