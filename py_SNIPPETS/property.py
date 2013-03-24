#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os

class A( object ):
    def __init__( self, name ):
        self._name = name

    @property
    def name( self ):
        print "zzZZ - @property"
        return self._name

    ## if this is commented, the attribute becomes ro
    @name.setter
    def name( self, name ):
        print "zzZZ - @name.setter"
        self._name = name

    @name.deleter
    def name( self ):
        print "zzZZ - @name.deleter"
        del self._name



## start
a = A("Bobo")

print ">>> getter"
print a.name
print ""

print ">>> setter"
a.name = "dada"
print ""

print ">>> deleter"
del a.name
print ""

print "READY."

