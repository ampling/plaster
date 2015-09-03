#! /usr/bin/env python3
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import http.client


def posts(payload):
    '''plugin for sprunge'''
    conn = http.client.HTTPConnection(url)
    conn.request("POST", "/", data="sprunge=" + payload)
    resp = conn.getresponse()
    print(resp.read())
    #print(r.status_code, r.reason)
