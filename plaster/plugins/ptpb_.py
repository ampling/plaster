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
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def plaster(payload, url):
    '''alt plugin for ptpb'''
    data = {'ptpb': payload}
    r = requests.post(url, data)
    
    #link = r.text
    print(r.status_code, r.reason)
    #print(r.headers)
    #return link # sucess
    code = r.status_code
    OK = r.status_code == requests.codes.ok
    try:
        if OK is True:
            print(r.text)
    except:
        print('ops')
        pass



    
    #link = r.text
    #print(r.status_code, r.reason)
    #print(r.headers)
    #return link #sucess
