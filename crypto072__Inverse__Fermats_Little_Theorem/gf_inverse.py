#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-02

Galois Field Inverse

Returns the inverse of a provided number within a specified Galois Field

Inverse
 * only values a that are coprime to the modulus m, have an inverse

 * by Fermat's Little Theorem
   a^{-1} = a^{p-2} mod p

 * by Euler's Theorem, this takes first to compute Phi(p)
   a^{-1} = a^{Phi(p)-1} mod p


example

4^{-1} mod 13 = 4^{12 - 1} mod 13 = 10
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)



### main ###
def main(argv=sys.argv[1:]):
    arg=4
    modulus=13
    ## get arguments, or set default values
    if 2 == len(argv):
        if 0 < len(argv[0]) and 0 < len(argv[1]):
            try:
                arg=int(argv[0])
                modulus=int(argv[1])
            except:
                die("usage: %s <arg> <modulus>\nOR call without arguments"%sys.argv[0] )
    if 0 >= modulus: die("FATAL: modulus must be greater than 0")

    ## apply finite field, sonce argument was outside
    if modulus <= arg: arg = arg%modulus

    print "arg = %d"%(arg)
    print "modulus = %d\n"%(modulus)

    ## check divisibility
    tmp = (modulus / arg)
    if arg * tmp == modulus:
        die("FATAL: inverse only exists if arg and modulus are coprime, %d divides %d times into %d"%(arg, tmp, modulus))

    ## compute inverse by Fermat's Little Theorem
    print "inverse by Fermat's Little Theorem"
    inv = arg**(modulus-2) % modulus

    print "inverse: %d"%inv



### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
