#! /usr/bin/env python3

import http.client

payload = "clbin=singsong"


def posts():
    conn = http.client.HTTPConnection("https://clbin.com/")
    conn.request("POST", "/", payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())

clbin()
