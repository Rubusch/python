#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os

class A( object ):
    def __init__( self, lst ):
        self._lst = []
        self._lst = lst

    @property
    def lst( self ):
        print "zzZZ - @property"
        ## return pointer, this may allow changing the pointee
#        return self._lst
        ## or, return shallow copy
        return [o for o in self._lst]

    ## enable this for appending elements, etc
    # @lst.setter
    # def lst( self, lst ):
    #     print "zzZZ - @lst.setter"
    #     self._lst = lst

    @lst.deleter
    def lst( self ):
        print "zzZZ - @lst.deleter"
        del self._lst



## start
a = A(["Fufu", "Nene", "Lolo"])

print ">>> getter (before)"
print "%s" % "\n" .join( map( str, a.lst ) )
print ""

## for setter, returning a pointee, this will show up "Data",
## if the setter returns a shallow copy, Data won't be added
print ">>> setter"
b = a.lst
b += ["Dada"]
print ""

## change element value
print ">>> change element"
a.lst[1] = "Fofi"
print ""

print ">>> getter (after)"
print "%s" % "\n" .join( map( str, a.lst ) )
print ""

print ">>> deleter"
del a.lst
print ""

print "READY."

