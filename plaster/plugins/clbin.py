#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import http.client
#import ssl

def posts(payload, url):
    '''plugin for clbin'''
    conn = http.client.HTTPConnection("url")
    conn.request("POST", "/", "clbin=" + payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())

