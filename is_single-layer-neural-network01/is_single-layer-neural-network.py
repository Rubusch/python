#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Code to train a single-layer neural network
# Assignment01 for Intelligent Systems
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-Sep-27


def die( self, msg = "" ):
    if 0 == len(msg): msg = "..."
    print "FATAL: " + msg
    sys.exit( -1 )



class Node(object):
## attributes (for overview)
    _name = "abc"
#    _value = "0"
    _up = []
    _down = []
    _edgeWeight = {}

    def __init__( self, name ):
        self._name = name
#        self._value = value
        self._up = []
        self._down = []
        self._edgeWeight = {}

    def __str__( self ):
        return self._name

    def __run__( self ):
# TODO calculate propagation?
        pass  

## private
    def _addNeighbor( self, dct, node, weight ):
        dct.append( node )
        self._edgeWeight.update({node:weight})

## public
    def upAdd( self, node, weight ):
        self._addNeighbor( self._up, node, weight )

    def up( self, idx ):
        return self._up[idx];

    def downAdd( self, node, weight ):
        self._addNeighbor( self._down, node, weight )

    def down( self, idx ):
        return self._down[idx];

    def downRun( self ):
        print self,
        for item in self._down:
            print " -> " +  str(item) + " [ label=" + str(self._edgeWeight.get(item)) + " ]"
            item.downRun()


    def upRun( self ):
# TODO
        pass    


###
if __name__ == '__main__':
    bias = Node( "bias" )
    net = Node( "net" )
    x1 = Node( "X1" )
    x2 = Node( "X2" )

    # x1 -> net
    x1.downAdd( net, 0.8 )
    net.upAdd( x1, 0.8 )

    # x2 -> net
    x2.downAdd( net, -0.5 )
    net.upAdd( x2, -0.5 )

    # bias -> net
    bias.downAdd( net, 2 )
    net.upAdd( bias, 2 )
    

    print "digraph G{"
    x1.downRun()
    x2.downRun()
    bias.downRun()
    print "}"

    print "# READY."

