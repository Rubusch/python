#!/usr/bin/python3
##
## changes from python2 to python3

import sys
print('python version: ', sys.version)

try:
    letz_cause_a_NameError

except NameError as err:
    print(err, '--> my error message')

print('READY.')
