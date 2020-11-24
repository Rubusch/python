#!/usr/bin/python3
##
## changes from python2 to python3

import sys
print('python version: ', sys.version)
print('')

## Python 3 adopted the now standard way of rounding decimals when it
## results in a tie (.5) at the last significant digits. Now, in
## Python 3, decimals are rounded to the nearest even number. Although
## it’s an inconvenience for code portability, it’s supposedly a
## better way of rounding compared to rounding up as it avoids the
## bias towards large numbers. For more information, see the excellent
## Wikipedia articles and paragraphs:
##
##    https://en.wikipedia.org/wiki/Rounding#Round_half_to_even
##    https://en.wikipedia.org/wiki/IEEE_floating_point#Roundings_to_nearest

## nearest even number: 16
print('15.5', round(15.5))

## nearest even number: 16
print('16.5', round(16.5))


print('')
print('READY.')
