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


Fermat's little theorem holds for all primes. Hence if a number does not fulfill
Fermat's Little Theorem, it is certainly not a prime.
    a^{prime} = a mod prime
    a^{prime-1} = 1 mod prime   ; as result of multiplying by its inverse

NOTE: The test fails for the rare Carmichael Numbers, e.g. 561

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
"""

import sys
import random

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def square_and_multiply(base, exp, modulus=0):
    
# FIXME 328^544 mod 545 = 1
    print "AAA\n%s base\n%s exp\n%s modulus"%(str(base), str(exp), str(modulus))    
    print "AAA\n%s base\n%s exp\n%s modulus"%(str(bin(base)), str(bin(exp)), str(bin(modulus)))    

    strexp = bin(exp)[2:]
    print "BBB '%s'"%strexp    

    res = 1
    for char in strexp:
        ## debug message
        print "binary: %s..."%char
        res = res*res
        if 0 != modulus: res = res % modulus
        if char == '1':
            res = res*base
            if 0 != modulus: res = res % modulus
            ## debugging
            print "\tidentified as '1', res = (res^2)*base = %d"%res
        else:
            print "\tidentified as '0': res = (res^2) = %d"%res
    print ""
    return res



### main ###
def main(argv=sys.argv[1:]):
    print "Fermat's Primality Test"

    arg=5
    ## get arguments, or set default values
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                arg=int(argv[0])
            except:
                die("usage: %s <arg>\nOR call without arguments"%sys.argv[0] )
    if 4 >= arg: die("FATAL: arg must be greater than 4")

#    base=random.randrange(2, arg-2) # pick a random number as base
    
    arg=545  
#    base=328  
    base=4  
    
    print "arg = %d, base = %d"%(arg, base)
    print "Is %d a prime number, by Fermat's Primality Test?\n"%arg

# TODO
#    print "FIXME: 545 becomes prime and 561 is identified as no prime..."    

    ## compute inverse by Euler's Theorem
    if 1 != square_and_multiply(base, arg-1, arg):
        print "%d is not a prime!"%arg
    else:
        print "%d can be a prime!"%arg


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
