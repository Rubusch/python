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

TODO   


example

TODO   


source

[p. TODO; Understanding Cryptography; Paar / Pelzel; Springer 2010]
"""


import sys

### tools ###

def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)



# TODO           

### main ###
def main(argv=sys.argv[1:]):
    die("TODO")    

    arg=14
    if 1 == len(argv):
        if 0 < len(argv[0]):
            try:
                arg=int(argv[0])
            except:
                die("usage: %s <arg>\nOR call without arguments"%sys.argv[0])


    ## result
#    print "\nZ[%d] contains %d integers, relatively prime to m=%d"%(arg, ephi, arg)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"

