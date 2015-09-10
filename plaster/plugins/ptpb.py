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
    time = 'yes'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def plaster():
    '''plugin for ptpb'''
    conn = http.client.HTTPSConnection(url)
    conn.request("POST", "/", "ptpb=" + payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())
