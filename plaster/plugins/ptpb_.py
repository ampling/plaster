#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################

import requests
#import ssl

url = "https://ptpb.pw"
payload = "ptpb=boo5"

def posts():
    '''alt plugin for ptpb'''
    r = requests.post(url, data=payload)
    print(r.status_code, r.reason)
    #print(r.text)
    print(r.headers)
