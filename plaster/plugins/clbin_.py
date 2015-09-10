# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import requests


def format():
    '''Availability'''
    txt = 'yes'
    img = 'yes'
    tls = 'yes'
    time = 'no'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form  

def plaster(payload, url):
    '''alt plugin for clbin'''
    r = requests.post(url, data="clbin=@" + payload)
    link = r.text
    print(r.status_code, r.reason)
    print(r.headers)
    return link # sucess
