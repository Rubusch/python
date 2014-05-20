#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-20

Square and Multiply algorithm

algorithm to facilitate calculating exponents by disassembling the operation into
a sequence of squaring and multiplication


example

4^13 = ?

take 13 as binary
    0b1101

for each '1' now compute square-multiply-by-base, for each '0' compute a squaring
only; start with 1^2*base for the first '1'

in case apply at each step a mod(n) operation

0b    1     1    0    1
((( 1^2*4 )^2*4 )^2 )^2*4


source

http://www.youtube.com/watch?v=rdMaG7s-lE4
http://en.wikipedia.org/wiki/Modular_exponentiation
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def square_and_multiply(base, exp, modulo=0):
    strexp = bin(exp)
    print strexp
    die("TODO") 
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

    ## get the greatest common divisor
    print "%d"%gcd(r0, r1)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

