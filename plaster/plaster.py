#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################
""" Plaster

Plaster is a configurable command-line pastebin client.
"""

from glob import glob
import fileinput
import configparser

config = configparser.ConfigParser()
config.sections()
config.read('plaster.conf')
config.sections()
plugin = 'sprunge_'
url = config[plugin]['url']

#for n in range(len(config.sections())):
#    plugin = config.sections()[n]
#    print(plugin)
    


from plugins import sprunge_ #fix needed


# helpers

def search_plugins(self):
    '''searches plugins folder'''
    list_plugins = glob("plugins/*.py")
    if best_plugin not in list_plugins:
        print("error: plugin not found")

# temp word fix
best_plugin = 'plugins/' + plugin + ".py"

for payload in fileinput.input():
    search_plugins(best_plugin)
    sprunge_.posts(payload, url) #fix needed
