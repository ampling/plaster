#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################
""" Plaster

Plaster is a friendly command-line pastebin client.
"""

import fileinput

for line in fileinput.input():
    print(line)

