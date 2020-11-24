#!/usr/bin/python3
##
## changes from python2 to python3

import sys
print('python version: ', sys.version)

try:
    print('Rise Exception')
    raise IOError("file error")

except IOError:
    print('Exception caught')

print('READY.')
