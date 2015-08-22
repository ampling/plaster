#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################

import requests


url = "http://sprunge.us"

def posts(payload):
    '''alt plugin for sprunge'''
    r = requests.post(url, data= "sprunge=" + payload)
    print(r.text)
    #print(r.status_code, r.reason)
