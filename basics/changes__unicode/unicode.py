#!/usr/bin/python3
##
## changes from python2 to python3
##
## Python 2 has ASCII str() types, separate unicode(), but no byte type. Now,
## in Python 3, we finally have Unicode (utf-8) strings, and 2 byte classes:
## byte and bytearrays.

import sys
print('python version: ', sys.version)

## unicode
print('strings are now utf-8: \u1F00\u03C1\u03B5\u03C4\u03AE!')

## type byte
print('python now has', type(b' bytes for storing data'))

## type bytearray
print('python now also has', type(bytearray(b'bytearrays')))

print('READY.')
