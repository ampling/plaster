#! /usr/bin/env python3
##############################################################################
#
# Copyright (c) [2015-08-06], ISC, [Ampling <plaster@ampling.com>]
#
##############################################################################

import requests


def posts(payload, url):
    '''alt plugin for sprunge'''
    r = requests.post(url, data= "sprunge=" + payload)
    link = r.text
    return link
