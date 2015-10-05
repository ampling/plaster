# -*- coding: utf-8 -*
########################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
########################################################################

import requests


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
    '''alt plugin for sprunge'''
    try:
        url = request_chain['url']
        data = request_chain['data']
        payload = {'sprunge': data}
        r = requests.post(url, payload)
        response = {
                'link': r.content.decode("utf-8"), 
                'code': r.status_code, 
                'reason': r.reason
                }
    except Exception as e:
        response = {'link': None, 'code': None, 'reason': e}
    finally:
        return response
