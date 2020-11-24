#!/usr/bin/python3
##
## changes from python2 to python3
##
## This change is particularly dangerous if you are porting code, or if you are
## executing Python 3 code in Python 2, since the change in integer-division
## behavior can often go unnoticed (it doesn’t raise a SyntaxError).




import sys
print('python version: ', sys.version)

## \ - Division: in python3 better always use: 'float(3)/2' or '3/2.0' instead
##     of a '3/2', and in python2 use a 'from __future__ import division'
print('3 / 2 =', 3 / 2, '[1.5]')

## \\ - Floor division: division that results into whole number adjusted to the
##      left in the number line
print('3 // 2 =', 3 // 2, '[1]')

## best practice: use always '.0'
print('3.0 / 2.0 =', 3 / 2, '[1.5]')
print('3.0 // 2.0 =', 3 // 2, '[1]')

print('READY.')
