# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import requests


def formula():
    '''Availability'''
    txt = 'yes'
    img = 'no'
    tls = 'no'
    time = 'no'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def post(payload, url):
    '''alt plugin for sprunge'''
    try:
        data = ('sprunge=' + payload)
        r = requests.post(url, data)
        link = r.text.strip()
        code = r.status_code
        reason = r.reason
        response = {'link': link, 'code': code, 'reason': reason}
    except Exception as e:
        response = {'link': 'na', 'code': None, 'reason': e}
    return response
