#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

import os

if os.path.exists('./test.txt'):
    os.remove('./test.txt')

text = """jack and jill went up the hill to fetch a pail of water
jack fell down and broke his crown
and jill came tumbling after
"""

# note: also the following is possible
# 0 means unbuffered
# 1 meands buffered
#FILE = open('test.txt', 'w', 0)

FILE = open('test.txt', 'w')
FILE.write(text)
FILE.close()

print "READY.\n"

