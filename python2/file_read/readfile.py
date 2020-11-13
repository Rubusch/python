#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

f=open('./test.txt')
# print file open mode
print f, '\n'

# print one line
print f.readline(), '\n'

# print the further content
print f.readlines(), '\n'

# close
f.close()

# print content in a nicer way
f=open('./test.txt')
for line in f:
    print line
f.close()
    
print "READY.\n"
