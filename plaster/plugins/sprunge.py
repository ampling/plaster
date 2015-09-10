# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import http.client


def format():
    '''Availability'''
    txt = 'no'
    img = 'no'
    tls = 'no'
    time = 'no'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def plaster(payload):
    '''plugin for sprunge'''
    conn = http.client.HTTPConnection(url)
    conn.request("POST", "/", data="sprunge=" + payload)
    resp = conn.getresponse()
    print(resp.read())
    #print(r.status_code, r.reason)
