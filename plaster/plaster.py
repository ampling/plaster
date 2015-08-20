#! /usr/bin/env python3

##############################################################################
#
# Copycenter (c) [2015-08-06], ISC, [Ampling]
#
##############################################################################
""" Plaster

Plaster is a configurable command-line pastebin client.
"""

import fileinput
from plugins import sprunge

#for line in fileinput.input():
#    print(line)

sprunge.posts()
