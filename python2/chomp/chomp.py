#!/usr/bin/python2
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

import sys


print 'test 1'
st = """The Python programming language
"""
st = st.rstrip('\n')


print 'read w/o linefeeds'
f = open('foo.txt','r')
foo = [line.rstrip('\n') for line in f.readlines()]

print foo
