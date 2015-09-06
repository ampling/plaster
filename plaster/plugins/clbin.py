# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import http.client
#import ssl

def format():
    '''Availability'''
    txt = 'yes'
    img = 'yes'
    tls = 'yes'
    time = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time}
    return form 

def plaster(payload, url):
    '''plugin for clbin'''
    conn = http.client.HTTPConnection("url")
    conn.request("POST", "/", "clbin=" + payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())

