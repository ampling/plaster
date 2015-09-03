#! /usr/bin/env python3
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import requests


def posts(payload, url):
    '''alt plugin for clbin'''
    r = requests.post(url, data="clbin=" + payload)
    link = r.text
    #print(r.status_code, r.reason)
    #print(r.headers)
    return link # sucess
