# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import http.client


def formula():
    '''Availability'''
    txt = 'yes'
    img = 'no'
    tls = 'no'
    time = 'no'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def post(data, url):
    '''plugin for sprunge'''
    try:    
        conn = http.client.HTTPConnection(url)
        conn.request("POST", "/", data="sprunge=" + data)
        resp = conn.getresponse()
        link = resp.read()
        code = (r.status_code + r.reason)
        response = {'link': link, 'code': code, 'reason': reason}
        return response
    except Exception as e:
        response = {'link': 'na', 'code': None, 'reason': e}
        return response
