#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import http.client
#import ssl

url = "https://clbin.com"

def posts():
    '''plugin for clbin'''
    conn = http.client.HTTPConnection("https://clbin.com/")
    conn.request("POST", "/", "clbin=" + payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())

