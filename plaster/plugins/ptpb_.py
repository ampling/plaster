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
    time = 'yes'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time}
    return form 

def plaster():
    '''alt plugin for ptpb'''
    r = requests.post(url, data="ptpb" + payload)
    link = r.text
    #print(r.status_code, r.reason)
    #print(r.headers)
    return link #sucess
