# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <post@ampling.com>]
#
##############################################################################

import requests


def tell_form():
    '''Availability'''
    txt = 'yes'
    img = 'yes'
    tls = 'yes'
    time = 'yes'
    nick = 'no'
    formula = {'txt': txt, 'img': img, 'tls': tls, 'time': time, 'nick': nick}
    return formula 

def tell_post(url, payload):
    '''alt plugin for ptpb'''
    try:
        data = {'c': payload}
        r = requests.post(url, files=data)
        # link = r.content.decode("utf-8").split()[10]
        link = r.content.decode("utf-8").rpartition(' ')[-1]
        code = r.status_code
        reason = r.reason
        response = {'link': link, 'code': code, 'reason': reason}
    except Exception as e:
        response = {'link': None, 'code': None, 'reason': e}
    finally:
        return response
