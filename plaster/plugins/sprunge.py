#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################

import http.client


url = "http://sprunge.us"
payload = "sprunge=boo6"

def posts():
    '''plugin for sprunge'''
    conn = http.client.HTTPConnection(url)
    conn.request("POST", "/", payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())
