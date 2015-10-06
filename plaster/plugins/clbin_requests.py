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
            'image': 'yes', 
            'tls': 'yes', 
            'time': 'no', 
            'login': 'no'
            }
    return formula  

def tell_post(request_chain):
    '''alt plugin for clbin'''
    try:
        url = request_chain['url']
        data = request_chain['data']
        time = request_chain['time']
        login = request_chain['login']
        payload = {'clbin': data}
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
