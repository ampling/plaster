# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import http.client
#import ssl

def formula():
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
    data = ('clbin=' + payload)
    conn = http.client.HTTPConnection(url)
    conn.request("POST", "/", data)
    #conn.request("POST", "/", "clbin=" + payload)
    resp = conn.getresponse()
    code = resp.status + resp.reason
    link = resp.read()
    response = {'link': link, 'code': code}
    return response
