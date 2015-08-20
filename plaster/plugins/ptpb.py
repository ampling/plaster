#! /usr/bin/env python3

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
