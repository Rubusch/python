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
## e.g. use as random.randrange( -1000, 1000 ) / 1000 


## plotting library
import matplotlib.pyplot as plt

def die( msg = "" ):
    if 0 == len(msg): msg = "..."
    print "FATAL: " + msg
    sys.exit( -1 )


class Node(object):
    _name = ""
    _nextlist = []
    _selftest = -1

    def __init__( self, name ):
        self._name = name
        self._nextlist = [];
        self._selftest = 0

    def __str__( self ):
        return self._name

    def addNext( self, nextnode, weight ):
        self._nextlist.append( [ nextnode, weight ] )

    def sizeNextList( self ):
        return len( self._nextlist )

    def selftest( self, val ):
        self._selftest += 1
        if 0 == self.sizeNextList():
            print self._selftest
        else:
            for nd in self._nextlist:
                nd[0].selftest( self._selftest )

    def forward( self, inval ):
        print "TODO " + str(inval)
        pass

    def backward( self, inval ):
        pass



class Monitor( object ):
    _inputnodes = []
    _netnode = None
    _trainingset = []
    _trainingtargets = []
    _stack = []

    def __init__( self ):
        self._netnode = Node( "net" )
        self._inputnodes = []
        self._trainingset = []
        self._trainingtargets = []
        self._stack = []

    def createNet( self ):
        self._inputnodes.append( Node("bias") )
        self._inputnodes.append( Node("x1") )
        self._inputnodes.append( Node("x2") )

        self._inputnodes[0].addNext( self._netnode, 2 )
        self._inputnodes[1].addNext( self._netnode, 0.8 )
        self._inputnodes[2].addNext( self._netnode, -0.5 )

        ## run selftest
        cnt = 0
        for nd in self._inputnodes:
            cnt += 1
            nd.selftest( 1 )
        print [str(cnt)]

## TODO
#        t2=-1  
#        class2x = [6, 7, 6, 10, 4]
#        class2y = [10, 7, 11, 5, 11]

        self._trainingset = []

        self._trainingset.append( [[1, 1, 1, 1, 1, 1], [1, 6, 3, 4, 3, 1], [8, 2, 6, 4, 1, 6]])
        self._trainingtargets.append(1)

        self._trainingsset.append( [[1, 1, 1, 1, 1], [6, 7, 6, 10, 4], [10, 7, 11, 5, 11]])
        self._trainingtargets.append(-1)

    def train( self ):
        for targetset in self._trainingset:
            for idxVal in 0:len( targetset[0] ):
                for idxNode in 0:len( self._inputnodes ):
                    inputvals = targetset[idxNode]
                    self._inputset[idxNode].forward( inputvals[idxVal])



    def _push( self, nd ):
        self._stack.append( nd )

    def _pop( self ):
        return self._stack.pop()

    
    def snapshot( self ):
        ## set up nodes
# TODO refac
        bias = Node( "bias" )
        net = Node( "net" )
        x1 = Node( "X1", "red" )
        x2 = Node( "X2", "blue" )

        
# TODO
        plt.plot( class1x, class1y, 'ro' )
# TODO
        plt.plot( class2x, class2y, 'bo' )

        xAxisMax = max(class1x + class2x)+1
        xAxisMin = min(class1x + class2x)-1
        yAxisMax = max(class1y + class2y)+1
        yAxisMin = min(class1y + class2y)-1

        # separator
#        plt.plot( [xAxisMin, xAxisMax], [yAxisMax, yAxisMin] )

        # scope
        plt.axis( [xAxisMin, xAxisMax, yAxisMin, yAxisMax] )

        plt.xlabel('x1')
        plt.ylabel('x2')
        plt.show()
        




###
learning_rate = 0.02
if __name__ == '__main__':

    monitor = Monitor()
    monitor.createNet()
    monitor.train()

    die( "STOP" )         



# TODO rm
## dotty
    # # x1 -> net
    # x1.downAdd( net, 0.8 )
    # net.upAdd( x1, 0.8 )

    # # x2 -> net
    # x2.downAdd( net, -0.5 )
    # net.upAdd( x2, -0.5 )

    # # bias -> net
    # bias.downAdd( net, 2 )
    # net.upAdd( bias, 2 )

    # dotty( [x1, x2, bias] )

    print "# READY."

