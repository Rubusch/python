#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# IMPORTANT: this implementation is meant as an educational demonstration only
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-September-12

Miller-Rabin's Primality Test

given the decomposition of an odd prime candidate p~
    p~ - 1 = 2^u * r

where r is odd; if we can find an integer a such that
    a^r != 1 mod p~    and   a^{r * 2^j} != p~ - 1 mod p~

for all j = {0, 1, ..., u-1}, then p~ is composite, otherwise
it is probably a prime


TEST:

Input
    prime candidate p~ with p~ - 1 = 2^u * r
    and security parameter s

Output
    statement "p~ composite" or "p~ is likely prime"

Algorithm
    for i = 1 to s:
        choose random a element of {2, 3, ..., p~ - 2}
        z = a^r mod p~
        if z != 1 and z != p~ - 1:
            for j = 1 to p~:
                z = z^2 mod p~
                if z = 1:
                    return "p~ is composite"
            if z != p~-1:
                return "p~ is composite"
    return "p~ is likely prime"
"""

import sys
import random

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)
    


### main ###
def main(argv=sys.argv[1:]):
    print "Miller-Rabin's Primality Test"
    arg=545

    ## get arguments, or set default values
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                arg=int(argv[0])
            except:
                die("usage: %s <arg>\nOR call without arguments"%sys.argv[0] )
    if 4 >= arg: die("FATAL: arg must be greater than 4")

    print "XXX arg %d"%arg    
    


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
