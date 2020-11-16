#!/usr/bin/python3
##
## changes from python2 to python3
import sys

print('python version: ', sys.version)
print('python version info: ', sys.version_info)

## print w/o  LF / CR
print('some text,', end='')
print(' some more text')

print('READY.')
