#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################

import requests


url = "https://clbin.com"
payload = "clbin=boo2"

def posts():
    '''alt plugin for clbin'''
    r = requests.post(url, data=payload)
    print(r.status_code, r.reason)
    print(r.text)
    #print(r.headers)
