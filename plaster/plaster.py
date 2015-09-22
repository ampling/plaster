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
        help="explain what is being done", action="store_true")
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
# BEGIN helper funtions 
#

def readin():
    '''Reads text or binary from stdin.'''
    try:
        payload = stdin.read()
        binary = False
    except KeyboardInterrupt:
        print('try:', 'plaster < example.txt' )
        exit(1)
    except:
        payload = stdin.buffer.read()
        binary = True
        pass
    return (payload, binary)

## Use early, use sparingly.
def _read_config():
    '''Parse configuration file, from top to bottom.'''
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        log.info('reading configuration file')
    except Exception as e:
            print(e)
            raise
    return config

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
    except Exception as e:
        log.info(e)
        pass
    return command

def _cull(command, mark): 
    '''Choose the best plugin for the job.'''
    global config
    sections = len(config.sections())
    for mark in range(mark, sections):
        try:
            # name of plugin
            name = config.sections()[mark]
            if args.verbose:
                print('##', name)
            match = _fnmatch(name)
            if match is False:
                if args.verbose:
                    print('*cull continues*')
            
            if match is True:
                form = _load(name).format()
                diff = set(form.keys()) - set(command.keys())
                sim = set(command.items()) & set(form.items())
                if len(sim) is len(command):
                    log.info('[OK] cull ')
                    break
                if len(sim) is not len(command):
                    log.info('skipped')
                    name = None
        except Exception as e:
            if args.verbose:
                print('BUG:', e)
            pass
    return (name, mark)

def _fnmatch(name):
    '''Check whether the plugins folder matches the desired plugin.'''
    list_plugins = glob(prefix + "/"  + "*.py")
    plugin_path = prefix + "/" + name + ".py" 
    if plugin_path in list_plugins:
        match = True
        log.info('[OK] fnmatch')
    else:
        match = False
        if args.verbose:
            print('WARNING: unable to match plugin:', name)
            print(str('  try: ls'), prefix + "/")
    return match 

def _load(name):
    '''Import a module by name.'''
    try:
        plugin_path = prefix + "/"  + name + ".py"
        spec = SourceFileLoader(name, plugin_path)
        module = spec.load_module()
        return module
    except Exception as e:
        log.info(e)
        print('problem loading plugin', name)
        raise

def paste(name, payload):
    '''send to bin'''
    try:
        global config
        url = config[name]['url']
        response = _load(name).post(payload, url)
    except Exception as e:
        log.info(e)
        pass
    return response


def plaster(command, payload):
    '''Adapt to all the things!'''
    global config
    config = _read_config()
    sections = (len(config.sections())-1)
    x = 0
    mark = 0
    for x in range(0, sections):
        '''compensating for downtime'''
        try:
            if mark > sections:
                if args.verbose:
                    print('exit 2')
                exit(1)
            cull = _cull(command, mark)
            name = cull[0]
            if name == None:
                if args.verbose:
                    print('exit 1')
                exit(1)
            mark = mark + 1
            response = paste(name, payload)
            try:
                reason = str(response['reason'])
                link = str(response['link'])
                code = str(response['code'])
            except Exception as e:
                if args.verbose:
                    print('WARNING:', 'bad plugin:', name)
                    print('  try reassigning variable', e)
                    print('  $EDITOR',  prefix + "/" + name + ".py" )
                continue
            if '200' in code: # might be better 200
                break
            elif code is None:
                log.info(code)
            print('end')
        except Exception as e:
            if args.verbose:
                print('WARNING: 0', e)
                print('*Plaster adapts*')
            mark = mark + 1
            # finds another
            pass
    return response

# add passwordeval
# def passwordeval():
#    gpg

#
# main
#

def __main__():
    payload = readin() 
    binary = payload[1]
    command = _get_command(binary)
    try:
        '''send hyperlink to stdout'''
        response = plaster(command, payload[0])
        reason = str(response['reason'])
        link = str(response['link'])
        code = str(response['code'])
        if 'Connection' in reason:
            log.error('network appears down')
        elif 'http' in link:
            print(str(link))
        else:
            log.error('unable to plaster')
            if not args.verbose:
                print('to debug, try plaster -v')
    except Exception as e:
        log.info(e)
        log.error("abandon all hope")
        pass
    

def __test__(): 
    log.info('debug mode')
    ###
    payload = 'test'
    binary = False
    command = _get_command(binary)
    global config
    config = _read_config()
    try:
        '''send link to stdout'''
        name = 'sprunge_requests'
        response  = paste(name, payload)
        reason = str(response['reason'])
        if 'Connection' in reason:
            print('connection error')
        
    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    __main__()
    # __test__()
