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
    img = 'no'
    tls = 'no'
    time = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time}
    return form 

def plaster(payload, url):
    '''alt plugin for sprunge'''
    r = requests.post(url, data= "sprunge=" + payload)
    link = r.text
    return link
