#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################

import requests


url = "https://ptpb.pw"

def posts():
    '''alt plugin for ptpb'''
    r = requests.post(url, data="ptpb" + payload)
    print(r.status_code, r.reason)
    print(r.text)
    #print(r.headers)
