#!/usr/bin/python3
##
## changes from python2 to python3

import sys
print('python version: ', sys.version)
print('')

## Fortunately, the input() function was fixed in Python 3 so that it always
## stores the user inputs as str objects. In order to avoid the dangerous
## behavior in Python 2 to read in other types than strings, we have to use
## raw_input() instead.
my_input = input('enter a number: ')
print('type: ',type(my_input))

print('READY.')
