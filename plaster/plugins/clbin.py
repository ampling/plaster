# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
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
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def post(payload, url):
    '''plugin for clbin'''
    conn = http.client.HTTPConnection("url")
    conn.request("POST", "/", "clbin=" + payload)
    resp = conn.getresponse()
    code = print(resp.status, resp.reason)
    link = resp.read()
    response = {'link': link, 'code': code}
    return response
