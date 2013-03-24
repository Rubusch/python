#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

def cube(x): return x*x*x

# usage map(function, sequence)
# calls function(item) for each of the sequence's items and returns a list of the return values
print map( cube, range(1, 11) )

print "READY.\n"

