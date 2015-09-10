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
    data = {'clbin': payload}
    r = requests.post(url, data)
    code = r.status_code
    OK = r.status_code == requests.codes.ok
    try:
        if OK is True:
            link = r.text
            #print(r.text)
    except:
        print('ops')
        pass
    
    return link 
