#! /usr/bin/env python3
##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import requests


def posts():
    '''alt plugin for ptpb'''
    r = requests.post(url, data="ptpb" + payload)
    link = r.text
    #print(r.status_code, r.reason)
    #print(r.headers)
    return link #sucess
