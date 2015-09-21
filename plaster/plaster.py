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
            log.info(e)
    return (config)

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
    sections = len(config.sections())
    for mark in range(mark, sections):
        try:
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
                    log.info('[OK] cull ')
                    break
                if len(sim) is not len(command):
                    log.info('skipped')
        except Exception as e:
            log.info(e)
            log.info('adapting...')
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
        print('problem matching plugin', name)
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
    '''send to net'''
    url = config[name]['url']
    response = _load(name).post(payload, url)
    return response


def plaster(command, payload):
    '''Adapt to all the things!'''
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
            ## paste
            response = paste(name, payload)
            link = str(response['link'])
            code = str(response['code'])
            if '200' in code: # might be better 200
                break
            else:
                log.info(code)
        except Exception as e:
            log.info(e)
            log.info('plaster adapting...')
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
        '''send link to stdout'''
        response = plaster(command, payload[0])
        link = str(response['link'].rstrip())
        code = str(response['code'])
        # reason = str(response['reason'])
        if 'http' in link:
            print(str(link))
        else:
            log.info(str(link))
            log.error('unable to plaster')
            if not args.verbose:
                print('to debug, try plaster -v')
    except Exception as e:
        log.info(e)
        log.error('all hope is lost')
        raise
    

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
        name = 'ptpb_curl'
        print(paste(name, payload))
    except:
        log.error('unable to plaster')
        raise


if __name__ == "__main__":
    __main__()
    # __test__()
