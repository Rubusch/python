#!/usr/bin/env python                                                                                                                                                                         # -*- coding: iso-8859-1 -*- 

import sys


print 'test 1'
st = """The Python programming language
"""
st = st.rstrip('\n')


print 'read w/o linefeeds'
f = open('foo.txt','r') 
foo = [line.rstrip('\n') for line in f.readlines()]

print 'foo'
