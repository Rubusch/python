#!/usr/bin/python3
##
## changes from python2 to python3

import sys
print('python version: ', sys.version)
print('')

## As we have already seen in the xrange section, some functions and
## methods return iterable objects in Python 3 now - instead of lists
## in Python 2.
##
## Since we usually iterate over those only once anyway, I think this
## change makes a lot of sense to save memory. However, it is also
## possible - in contrast to generators - to iterate over those
## multiple times if needed, it is only not so efficient.
##
## And for those cases where we really need the list-objects, we can
## simply convert the iterable object into a list via the list()
## function.

print(range(3))
print(type(range(3)))
print(list(range(3)))

## Some more commonly used functions and methods that don’t return lists anymore in Python 3:
##
##    zip()
##
##    map()
##
##    filter()
##
##    dictionary’s .keys() method
##
##    dictionary’s .values() method
##
##    dictionary’s .items() method

print('READY.')
