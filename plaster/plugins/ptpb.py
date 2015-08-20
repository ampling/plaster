#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################

import http.client
import ssl

payload = "ptpb=singsong"

def posts():
    conn = http.client.HTTPSConnection("https://ptpb.pw/")
    conn.request("POST", "/", payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())

posts()
