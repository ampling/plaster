#! /usr/bin/env python3

import http.client

payload = "sprunge=sing"


def posts():
    conn = http.client.HTTPConnection("sprunge.us")
    conn.request("POST", "/", payload)
    resp = conn.getresponse()
    print(resp.status, resp.reason)
    print(resp.read())

