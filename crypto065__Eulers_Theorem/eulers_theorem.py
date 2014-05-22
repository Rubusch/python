#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-May-20


Euler's Theorem

let a and m be integers with gcd(a,m) = 1, then
    a^{Phi(m)} = 1 mod(m)

it returns the exponent for which a will result the identity 1 mod m

this is a generalization of Fermat's little theorem to any integer moduli, i.e.
moduli that are not necessarily primes

it is easy to show that Fermat's Little Theorem is a special case of Euler's
Theorem. If p is a prime, it holds that Phi(p) = (p^1 - p^0) = p - 1

If we use this value for Euler's theorem, we obtain:
a^{Phi(p)} = a^{p-1} = 1 mod p

which is exactly Fermat's Little Theorem


example

let m = 12 and a = 5; first we compute Euler's phi function of m:
Phi(12) = Phi(2^2 * 3) = (2^2 - 2^1) (3^1 - 3^0) = (4-2) (3-1) = 4

Now we can verify Euler's theorem:
    5^{Phi(12)} = 5^4 = 25^2 = 625 = 1 mod 12


source

[p. 167; Understanding Cryptography; Paar / Pelzel; Springer 2010]
"""


import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


def factorize(m):
    ## get factors of m
    factors = []
    exponents = []

    val = m
    for num in range(2, m):
        if 0 == (val % num):
            factors.append(num)
            cnt = 0
            while 0 == val % num:
                cnt+=1
                val = val / num
            exponents.append(cnt)
            if num > val: break
    return (factors, exponents)


def phi(m, factors, exponents):
    ## compute Phi(m), the number of all integers in Z[m], relatively prime to m
    res = 1
    for idx in range(len(factors)):
        res *= (factors[idx]**exponents[idx] - factors[idx]**(exponents[idx]-1) )
    return res


def eulers_theorem(arg,ephi,base):
    return (arg**ephi) % base


### main ###
def main(argv=sys.argv[1:]):
    arg=5
    base=12
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                arg=int(argv[0])
            except:
                die("usage: %s <arg> <base>\nOR call without arguments"%sys.argv[0])

    ## find prim factors
    print "factorize(base)"
    (factors, exponents) = factorize(base)

    print "\tfactors:\t[%s]"%', '.join(map(str,factors))
    print "\texponents:\t[%s]"%', '.join(map(str,exponents))

    ## Phi(m)
    print "\nphi(m) = ",
    ephi = phi(base, factors, exponents)
    print ephi

    print "\nEuler's theorem:",
    eulers = eulers_theorem(arg, ephi, base)

    ## result
    print "%d^%d = %d mod %d"%(arg, ephi, eulers, base)
    print ""


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

