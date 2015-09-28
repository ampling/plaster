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

def post(url, data):
    '''plugin for sprunge'''
    try:
        conn = http.client.HTTPConnection(url)
        conn.request("POST", "/", "sprunge=" + data)
        print('dog')
        resp = conn.getresponse()
        link = resp.read()
        reason = 'cats'
        code = 'cats'
        # code = (resp.status_code + resp.reason)
        response = {'link': link }
        print(response)
        return response
    except Exception as e:
        # raise
        response = {'link': 'na', 'code': None, 'reason': e}
        return response

