# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import http.client
import ssl

def tell_form():
    '''Availability'''
    txt = 'yes'
    img = 'yes'
    tls = 'yes'
    time = 'yes'
    nick = 'no'
    formula = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return formula 

def tell_post(url, data):
    '''plugin for ptpb'''
    try:    
        conn = http.client.HTTPSConnection(url)
        conn.request("POST", "/", data)
        resp = conn.getresponse()
        # code = resp.status + resp.reason
        link = resp.read().decode("utf-8")
        response = {'link': link}
        return response
    except Exception as e:
        response = {'link': 'na', 'code': None, 'reason': e}
        return response
