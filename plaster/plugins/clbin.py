# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
########################################################################

import http.client
import ssl

def tell_form():
    '''Availability'''
    formula = {
            'txt': 'yes', 
            'img': 'yes', 
            'tls': 'yes', 
            'time': 'no', 
            'login': 'no'
            }
    return formula

def tell_post(request_chain):
    '''plugin for clbin'''
    try:
        url = request_chain['url'].rpartition('//')[-1]
        data = request_chain['data']
        time = request_chain['time']
        login = request_chain['login']
        payload = ('clbin=' + data)
        conn = http.client.HTTPConnection(url)
        conn.request("POST", "/", payload)
        resp = conn.getresponse()
        response = {
                'link': resp.read().decode('utf-8'), 
                'code': resp.status,
                'reason': resp.reason
                }
        return response
    except Exception as e:
        response = {'link': None, 'code': None, 'reason': e}
        return response
