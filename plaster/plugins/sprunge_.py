#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################

import requests


url = "http://sprunge.us"
payload = "sprunge=boo7"

def posts():
    '''alt plugin for sprunge'''
    r = requests.post(url, data=payload)
    print(r.status_code, r.reason)
    #print(r.text)
    print(r.headers)
