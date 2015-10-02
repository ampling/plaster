# -*- coding: utf-8 -*
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import requests


def tell_form():
    '''Availability'''
    txt = 'yes'
    img = 'no'
    tls = 'no'
    time = 'no'
    nick = 'no'
    formula = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return formula 

def tell_post(url, data):
    '''alt plugin for sprunge'''
    try:
        d = {'sprunge': data}
        r = requests.post(url, d)
        link = r.content.decode("utf-8")
        code = r.status_code
        reason = r.reason
        response = {'link': link, 'code': code, 'reason': reason}
    except Exception as e:
        response = {'link': None, 'code': None, 'reason': e}
    finally:
        return response
