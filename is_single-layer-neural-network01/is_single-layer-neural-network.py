#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Code to train a single-layer neural network
# Assignment01 for Intelligent Systems
#
## training set
# Class1 (t=1): (1,8), (6,2), (3,6), (4,4), (3,1), (1,6)
# Class2 (t=-1): (6,10), (7,7), (6,11), (10,5), (4,11)
#
## tasks
# a) plot the training set with the initial separation line where the two classes are displayed in different colors   [3 pts]
# b) implement the delta rule and apply it for all points from the test set, with a learning rate of ny = 1/50   [20 pts]
# c) plot the new separation line   [3 pts]
# d) train the perceptron until all the points are correctly classified and plot the final decision boundary line   [10 pts]
# e) is it a good solution? Discuss potential problems that may arise.   [4 pts]
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-Sep-27

## sys.exit()
import sys

## random number, random() and randrange()
import random

## plotting library
import matplotlib.pyplot as plt

def die( msg = "" ):
    if 0 == len(msg): msg = "..."
    print "FATAL: " + msg
    sys.exit( -1 )

def dotty( nodes ):
    print "digraph G{"
    print "node [style=filled];"
    print "edge [arrowhead=none,arrowtype=normal,arrowtail=dot];"
    for node in nodes:
        node.downDescend();
    print "}"


class Node(object):
## attributes (for overview)
    _name = "abc"
    _up = []
    _down = []
    _edgeWeight = {}

    _xval = "0"
    _bias = None
    _net = None

    _dotColor = ""

    def __init__( self, name, color="" ):
        self._name = name
        self._xval = random.randrange( 0, 100 ) / 100
        self._up = []
        self._down = []
        self._edgeWeight = {}
        self._dotColor = color

    def __str__( self ):
        return self._name

#    def __run__( self ):
# TODO calculate propagation?
#        pass  

## private
    def _addNeighbor( self, dct, node, weight ):
        if "bias" == str(node):
            self._bias = node
#        elif "net" == str(node):
#            self._net = node
        else:
            dct.append( node )
        self._edgeWeight.update({node:weight})

## public
    def upAdd( self, node, weight ):
        self._addNeighbor( self._up, node, weight )

    def up( self ):
        return self._up;

    def downAdd( self, node, weight ):
        self._addNeighbor( self._down, node, weight )

    def down( self ):
        return self._down;

    def xval( self ):
        return self._xval

    def setXval( self, x ):
# TODO in case here apply node function?
        self._xval = x




#    def _getNewWeights( self, weight ):
## algorithm
#
#    1) Perform the forwardpropagation phase for an input pattern and calculate
#       the output error
#    2) Change all weight values of each weight matrix using the formula
#       weight(old) + learning rate * output error * output(neurons i) * output(neurons i+1) * ( 1 - output(neurons i+1) )
#    3) Go to step 1
#    4) The algorithm ends, if all output patterns match their target patterns
#        return weight + learning_rate * output_error * output[idx] * output[idx+1] * (1 - output[i+1])

    def _computeInput( self ):
        for item in self.up():
            w += self._edgeWeight( item ) * self._input( item ) # TODO input( item ), a dict for second input value  

    def forwardPropagation( self ):
# TODO         
        f = 0
        w0 = 0
        if self._bias:
            w0 = self._edgeWeight.get( self._bias )
        for item in self._down:
            wi = self._edgeWeight.get(item)
            xi = self._xval
            f += wi * xi
        f += w0

    def forwardDotty( self ):
        if self._dotColor: print str(self) + "[ fillcolor=" + self._dotColor + " ]"
        for item in self._down:
## in case we need different upward settings
#            try:
#                item.up().index( self ) # contains an upward reference?
#            except ValueError:
#                TODO: implement here upward connections
            print str(self) + " -> " + str(item) + " [ label=" + str(self._edgeWeight.get(item)) + " ];"
            item.forwardDotty()






#    def backwardDotty( self ):
# TODO
#        pass    

    def backwardPropagation( self ):
# TODO
        pass    






###
learning_rate = 0.02
if __name__ == '__main__':

    ## set up nodes
    bias = Node( "bias" )
    net = Node( "net" )
    x1 = Node( "X1", "red" )
    x2 = Node( "X2", "blue" )

## training set
    t1=1  
    class1x = [ 1, 6, 3, 4, 3, 1 ]
    class1y = [ 8, 2, 6, 4, 1, 6 ]
    plt.plot( class1x, class1y, 'ro' )

    t2=-1  
    class2x = [6, 7, 6, 10, 4]
    class2y = [10, 7, 11, 5, 11]
    plt.plot( class2x, class2y, 'bo' )

    xAxisMax = max(class1x + class2x)+1;
    xAxisMin = min(class1x + class2x)-1;
    yAxisMax = max(class1y + class2y)+1;
    yAxisMin = min(class1y + class2y)-1;

    # separator
    plt.plot( [xAxisMin, xAxisMax], [yAxisMax, yAxisMin] )

    # scope
    plt.axis( [xAxisMin, xAxisMax, yAxisMin, yAxisMax] )

    plt.ylabel('some numbers')
    plt.show()




## dotty
    # x1 -> net
    x1.downAdd( net, 0.8 )
    net.upAdd( x1, 0.8 )

    # x2 -> net
    x2.downAdd( net, -0.5 )
    net.upAdd( x2, -0.5 )

    # bias -> net
    bias.downAdd( net, 2 )
    net.upAdd( bias, 2 )

    dotty( [x1, x2, bias] )

    print "# READY."

