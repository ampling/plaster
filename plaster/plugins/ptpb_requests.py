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
    img = 'yes'
    tls = 'yes'
    time = 'yes'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def post(payload, url):
    '''alt plugin for ptpb'''
    data = {'c=': payload}
    r = requests.post(url, data)
    code = r.status_code
    OK = r.status_code == requests.codes.ok
    link = r.text
    reason = r.reason
    response = {'link': link, 'code': code, 'reason': reason}
    return response