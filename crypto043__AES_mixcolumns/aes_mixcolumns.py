#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-Mar-19

sources:
Book: Understanding Cryptography, Christof Paar, Jan Pelzl (c) Springer 2010

http://en.wikipedia.org/wiki/Advanced_Encryption_Standard
http://en.wikipedia.org/wiki/Rijndael_mix_columns
http://en.wikipedia.org/wiki/Rijndael_key_schedule

Chris Veness' AES implementation: http://www.movable-type.co.uk/scripts/aes.html
(c) 2005-2008 Chris Veness. Right of free use is granted for all
commercial or non-commercial use. No warranty of any form is offered.

functions from AES python port
(c) 2009 by Markus Birth <markus@birth-online.de>
"""

import sys

def die(msg):
    print msg
    sys.exit(1)

## Galois Multiplication
## addition = XOR operation
## multiplication = left shift, then modular reduction by P(x)
##
## here a is a 4-vector of the specific column,
## while b is a 4-vector of the same values x2, in case they are having a
## carry and would exceed the GF(2^8) limit, this is removed
## then, XORing the elements, either a signle a is taken,
## or a b, means 2a are taken, or
## a corresponding a and it's b, means 3a are taken, corresponding to the matrix
##
## Mix Columns operation, per column (here a is one column)
##
##         / 2 3 1 1 \     / a0 \
##        |  1 2 3 1  |   |  a1  |
##  C ==  |  1 1 2 3  | * |  a2  |
##         \ 3 1 1 2 /     \ a3 /
##
def mix_columns(s, Nb=4):
    for c in range(4):
        a = [0] * 4
        b = [0] * 4

        for i in range(4):
            a[i] = s[i][c]
            b[i] = s[i][c]<<1 ^ 0x011b if s[i][c]&0x80 else s[i][c]<<1
            ## explicitly written
            # if s[i][c] & 0x80:
            #     b[i] = s[i][c]<<1 ^ 0x011b
            # else:
            #     b[i] = s[i][c]<<1

        print "a ",a
        print "b ",b

        s[0][c] = b[0] ^ a[1] ^ b[1] ^ a[2] ^ a[3]
        print "s[0][%d] = b[0] ^ a[1] ^ b[1] ^ a[2] ^ a[3] = %x ^ %x ^ %x ^ %x ^ %x = %x" % (c, b[0], a[1], b[1], a[2], a[3], s[0][c])

        s[1][c] = a[0] ^ b[1] ^ a[2] ^ b[2] ^ a[3]
        print "s[1][%d] = a[0] ^ b[1] ^ a[2] ^ b[2] ^ a[3] = %x ^ %x ^ %x ^ %x ^ %x = %x" % (c, a[0], b[1], a[2], b[2], a[3], s[1][c])

        s[2][c] = a[0] ^ a[1] ^ b[2] ^ a[3] ^ b[3]
        print "s[2][%d] = a[0] ^ a[1] ^ b[2] ^ a[3] ^ b[3] = %x ^ %x ^ %x ^ %x ^ %x = %x" % (c, a[0], a[1], b[2], a[3], b[3], s[2][c])

        s[3][c] = a[0] ^ b[0] ^ a[1] ^ a[2] ^ b[3]
        print "s[3][%d] = a[0] ^ b[0] ^ a[1] ^ a[2] ^ b[3] = %x ^ %x ^ %x ^ %x ^ %x = %x" % (c, a[0], b[0], a[1], a[2], b[3], s[1][c])

        print ""

    return s

def printstate(s):
    for row in range(4):
        for col in range(4):
            ## dec
            val = s[row][col]
            if val <= 9: print " 0%d"%(val),
            else: print " %d"%(val),
            ## hex
#            print " %#x"%(s[row][col]),
        print ""
    print "---"

if __name__ == "__main__":

    Nb = 4
    state = [ [0]*Nb, [0]*Nb, [0]*Nb, [0]*Nb ]
    for i in range(4*Nb): state[i%4][i/4] = i

    printstate(state)

    state = mix_columns(state)

    printstate(state)

    print "READY."
