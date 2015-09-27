# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import http.client
import ssl

def formula():
    '''Availability'''
    txt = 'yes'
    img = 'yes'
    tls = 'yes'
    time = 'yes'
    nick = 'no'
    form = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return form 

def post(url, data):
    '''plugin for ptpb'''
    try:    
        
        print('.')
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", "/", data)
        print('cats')
        resp = conn.getresponse()
        # code = resp.status + resp.reason
        link = resp.read()
        print(link)
        # response = {'link': link}
        return response
    except Exception as e:
        raise
        response = {'link': 'na', 'code': None, 'reason': e}
        return response
