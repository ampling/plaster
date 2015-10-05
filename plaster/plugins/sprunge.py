# -*- coding: utf-8 -*-
########################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
########################################################################

import http.client


def tell_form():
    '''Availability'''
    formula = {
            'text': 'yes', 
            'image': 'no', 
            'tls': 'no', 
            'time': 'no', 
            'login': 'no'
            }
    return formula

def tell_post(request_chain):
    '''plugin for sprunge'''
    try:
        url = request_chain['url'].rpartition('://')[-1]
        data = request_chain['data']
        conn = http.client.HTTPConnection(url)
        conn.request("POST", "/", "sprunge=" + data)
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

