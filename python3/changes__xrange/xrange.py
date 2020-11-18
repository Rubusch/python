#!/usr/bin/python3
##
## changes from python2 to python3
##
##
## NO MORE xrange() IN PYTHON3!
##
## The usage of xrange() is very popular in Python 2.x for creating an iterable
## object, e.g., in a for-loop or list/set-dictionary-comprehension.
## The behavior was quite similar to a generator (i.e., “lazy evaluation”), but
## here the xrange-iterable is not exhaustible - meaning, you could iterate over
## it infinitely.
##
## Thanks to its “lazy-evaluation”, the advantage of the regular range() is that
## xrange() is generally faster if you have to iterate over it only once (e.g.,
## in a for-loop). However, in contrast to 1-time iterations, it is not
## recommended if you repeat the iteration multiple times, since the generation
## happens every time from scratch!
##
## In Python 3, the range() was implemented like the xrange() function so that a
## dedicated xrange() function does not exist anymore (xrange() raises a
## NameError in Python 3).
##
## REFERENCE: https://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html

import sys

## performance, time measuring
import timeit

## python2: range() is slow, use xrange()
def test_range(n):
    for i in range(n):
        pass

## python2: xrange does not exist anymore in python3, use range()
#def test_xrange(n):
#    for i in xrange(n):
#        pass

print('python version: ', sys.version)

n = 10
t = timeit.timeit("test_range(%d)" % n, setup="from __main__ import test_range")
print('\ntiming range() %s' %t)

print('READY.')
