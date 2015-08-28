#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import http.client
#import ssl

def posts():
    '''plugin for ptpb'''
    conn = http.client.HTTPSConnection(url)
    conn.request("POST", "/", "ptpb=" + payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())
