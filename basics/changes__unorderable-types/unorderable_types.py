#!/usr/bin/python3
##
## Another nice change in Python 3 is that a TypeError is raised as warning if
## we try to compare unorderable types.

import sys
print('python version: ', sys.version)

try:
    print("[1, 2] > 'foo' = ", [1, 2] > 'foo')
    print("(1, 2) > 'foo' = ", (1, 2) > 'foo')
    print("[1, 2] > (1, 2) = ", [1, 2] > (1, 2))
except TypeError as te:
    print("XXX TypeError caught XXX")

print('READY.')
