#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-04

Euclidian Algorithm

input: positive integers r[0] and r[1] with r[0] > r[1]
output: gcd(r[0], r[1])   ; greatest common divisor
initialization: i = 1


algorithm:
gcd(r[0], r[1]):
    do
        i = i+1
        r[i] = r[i-1] mod r[i-1]
    while r[i] != 0
    return gcd(r[0], r[1]) = r[i-1]


example:
gcd(27, 21) = gcd(21, 6) = gcd(6, 3) = gcd(3, 0) = 3
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


def gcd(r0, r1):
    print "gcd(%d, %d)" %(r0,r1)
# TODO
    

### main ###
def main(argv=sys.argv[1:]):
    r0=27
    r1=21
    if 2 == len(argv):
        if 0 < len(argv[0]) and 0 < len(argv[1]):
            try:
                r0=int(argv[0])
                r1=int(argv[1])
            except:
                die("usage: %s <r0> <r1>\nOR call without arguments"%sys.argv[0])

    if r0 <= r1: die("r0 must be greater than r1")

    # greatest common divisor
    gcd(r0, r1)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

