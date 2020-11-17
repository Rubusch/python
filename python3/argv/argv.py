#!/usr/bin/python3
#
# for python2 use: /usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

import sys

for item in sys.argv[1:]:
    print("args '%s'" % item)

if (len(sys.argv)-1) != 2:
    print("the number of arguments was not two")
else:
    print("two arguments passed")

print("READY.")
