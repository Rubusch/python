#!/usr/bin/python3
##
## changes from python2 to python3

import sys
print('python version: ', sys.version)
print('')

## print arguments
print('python version info: ', sys.version_info)

## no  LF / CR
print('some text,', end='') ## avoid EOL
print(' some more text')

## print several objects
print('a', 'b')

print('READY.')
