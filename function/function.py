#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

def fib(n):
    """print a fibonacci series up to n"""
    result = []
    a, b = 0, 1
    while b < n:
        print b,
        result.append(b)
        a, b = b, a+b
    return result

# call
f2000 = fib(2000)
print f2000, "READY.\n"
