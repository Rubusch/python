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


## starting python 3.6
foo={1, 2, 3}
print(f"python 3.6 allows for this printing, foo: {foo}")

print('READY.')
