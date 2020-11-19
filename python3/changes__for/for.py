#!/usr/bin/python3
##
## changes from python2 to python3
##
## Good news is: In Python 3.x for-loop variables don’t leak into the global namespace anymore!

import sys
print('python version: ', sys.version)

i = 1
print('before: i =', i)

print('comprehension:', [i for i in range(5)])

print('after: i =', i) # this returned in python2: '4', and in python3: '1'


print('READY.')
