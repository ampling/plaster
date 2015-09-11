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
    img = 'no'
    tls = 'no'
    time = 'no'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def post(payload, url):
    '''alt plugin for sprunge'''
    r = requests.post(url, data= str("sprunge=" + payload))
    link = r.text
    return link
