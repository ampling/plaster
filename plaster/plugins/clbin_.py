#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import requests


url = "https://clbin.com"

def posts(payload):
    '''alt plugin for clbin'''
    r = requests.post(url, data="clbin=" + payload)
    print(r.status_code, r.reason)
    print(r.text)
    #print(r.headers)
