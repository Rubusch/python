#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

def f(x): return x % 2 != 0 and x % 3 !=0

# usage of filter( function, sequence ):
# returns a sequence consisting of those items from the sequence for which
# function(item) is true; the result will be of the same type, otherwise
# defaults to list
print filter( f, range(2, 25) )

print "READY.\n"
