#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

def add(x,y):  return x+y

# usage: reduce(function, sequence)
# returns a single value constructed by calling the binary function "function" on the first two items of the sequence, 
# then on the result and the next item, and so on
print 'simple reduce', reduce( add, range( 1, 11 ) )

# a third argument can be passed to indicate the starting value; 
# in this case the starting value is returned for an empty sequence, 
# and the function is first applied to the starting value and the 
# first sequence item, then to the result and the next item, and so on
def sum(seq):
    def add(x,y): return x+y
    return reduce(add, seq, 0)

print 'third element reduce', sum( range(1, 11) )

print "READY.\n"

