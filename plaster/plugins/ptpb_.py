# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import requests


def format():
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
    data = {'ptpb=': payload}
    try:
        r = requests.post(url, data)
        print(r.status_code, r.reason)
        code = r.status_code
        OK = r.status_code == requests.codes.ok
        if OK is True:
            print(r.text)
    except:
        print('ops')
        pass

