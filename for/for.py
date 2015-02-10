#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

arr = ['cat', 'mouse', 'monkey']
print "...by element:"
for x in arr:
    print x

print "...by index:"
for x in range(len(arr)):
    print x, arr[x]

print "READY.\n"
