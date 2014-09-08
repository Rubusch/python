#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-08

Fermat's Primality Test

    a^{C-1} = 1 mod C


Fermat's little theorem holds for all primes:
    a^{prime} = a mod prime
    a^{prime-1} = 1 mod prime   ; as result of multiplying by its inverse

Input
    prime candidate p~ and security parameter s

Output
    statement "p~ is composite" or "p~ is likely prime"

Algorithm
    for i = 1 to s:
        choose random a element of {2, 3, ..., p~ -2}
        if a^{p~ - 1} != 1 mod p~:
            return "p~ is a composite"
    return "p~ is likely prime"

NOTE: The test fails for the rare Carmichael Numbers, e.g. 561
"""

import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


### main ###
def main(argv=sys.argv[1:]):
    print "Fermat's Primality Test"

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
    if 1 >= modulus: die("FATAL: modulus must be greater than 0")

    ## apply finite field, sonce argument was outside
    if modulus <= arg: arg = arg%modulus

    print "arg = %d"%(arg)
    print "modulus = %d\n"%(modulus)

    ## check divisibility
    if gcd(arg, modulus) != 1:
        die("FATAL: inverse only exists if arg and modulus are coprime, %d divides into %d"%(arg, modulus))

    ## find prim factors
    (factors, exponents) = factorize(modulus)
    print "factors:\t[%s]"%', '.join(map(str,factors))
    print "exponents:\t[%s]"%', '.join(map(str,exponents))

    ## Phi(m)
    print "\nphi(%d) = "%(modulus),
    ephi = phi(modulus, factors, exponents)
    print ephi

    ## compute inverse by Euler's Theorem
    inv = arg**(ephi-1) % modulus
    print "inverse: %d"%inv



### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
