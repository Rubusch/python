#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-19

Euler's Phi Function

The number of integers in Z[m] relatively prime to m is denoted by Phi(m)

The theorem answers the question of how many numbers in a set are relatively
prime to m.

Let m have the following canonical factorization
    m = p[1]^{e1} * p[2]^{e2} * p[3]^{e3} * ... p[n]^{en}

where the p[i] are distinct prime numbers and e[i] are positive integers, then
    Phi(m) = Product[i=1; n]( p[i]^{ei} - pi^{ei-1} )


algorithm:

TODO          


example:

let m = 240; the factorization of 240 in the canonical factorization form is
    m = 240 = 16 * 15 = 2^4 * 3 * 5 = p1^{e1} * p2^{e2} * p3^{e3}

there are 3 distinct prime factors, i.e. n = 3. The value for Euler's phi
function follows then as:
    Phi(m) = (2^4 - 2^3)(3^1 - 3^0)(5^1 - 5^0) = 8 * 2 * 4 = 64

that means, 64 integers in the range {0,1,...,239} are coprime to m = 240

it is obvious that this method is straightforward in comparison to compute all
240 gcds.

source
[p. 166; Understanding Cryptography; Paar / Pelzel; Springer 2010]
"""


# TODO
import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def gcd(r0, r1):
    ## return the greatest common divisor
    ## identified by the Euclidean Algorithm
    while r1 != 0:
        tmp = r1
        r1 = r0 % r1
        r0 = tmp
    return r0

def phi(m):
    
    ## get factors of m
    factors = []
# TODO  

    ## get exponents of factors
    exponents = []
# TODO  

    ## compute Phi(m)
# TODO
    res = 1
    for idx in range(factors):
        res *= (factors[idx]^exponent[idx] - factors[idx]^(exponent[idx]-1))
    return res

#def extended_gcd(r0, r1):
#    print "\tinit"
#    s = 0; old_s = 1
#    t = 1; old_t = 0
#    r = r1; old_r = r0
#
#    print "\told_r = %d,\tr = %d"%(old_r, r)
#    print "\told_s = %d,\ts = %d"%(old_s, s)
#    print "\told_t = %d,\tt = %d"%(old_t, t)
#    print ""
#
#    while r != 0:
#        quot = old_r / r
#        (old_r, r) = (r, old_r - quot * r)
#        (old_s, s) = (s, old_s - quot * s)
#        (old_t, t) = (t, old_t - quot * t)
#
#        print "\t\tanother round..."
#        print "\t\tquot = %d"%quot
#        print "\t\told_r = %d,\tr = %d"%(old_r, r)
#        print "\t\told_s = %d,\ts = %d"%(old_s, s)
#        print "\t\told_t = %d,\tt = %d"%(old_t, t)
#        print ""
#
#    print "Bézout coefficients: %d and %d"%(old_s, old_t)
#    print "greatest common divisor: %d"%old_r
#    print "quotients by the gcd: %d and %d"%(t, s)


### main ###
def main(argv=sys.argv[1:]):
    r0=27
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                r0=int(argv[0])
            except:
                die("usage: %s <r0> <r1>\nOR call without arguments"%sys.argv[0])

    ## get the greatest common divisor
    for elem in range(r0):
        res = gcd(r0, elem)
        print "gcd(%.2d, %.2d) = %d"%(r0, elem, res),
        if res == 1: print "-> coprime"
        else: print ""


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

