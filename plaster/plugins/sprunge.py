# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import http.client


def format():
    '''Availability'''
    txt = 'yes'
    img = 'no'
    tls = 'no'
    time = 'no'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def post(payload, url):
    '''plugin for sprunge'''
    conn = http.client.HTTPConnection(url)
    conn.request("POST", "/", data="sprunge=" + payload)
    resp = conn.getresponse()
    link = resp.read()
    code = (r.status_code + r.reason)
    response = {'link': link, 'code': code}
    return response
