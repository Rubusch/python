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
#import random
## e.g. use as random.randrange( -1000, 1000 ) / 1000 

## plotting library
import matplotlib.pyplot as plt

def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )

class Perceptron( object ):
    ## overview
    _weightlist = []   # weights (size of class 1 + 2)
#    _ylist = []        # intermediate y
    _trainingset2 = [] # training data (class 1 and 2)
    _targetlist2 = []  # targets (size of class 1 + 2)
    _learningrate = [] # provided
    _epochdwlist = []  # for plotting
    _epochtime = []    # for plotting

    def __init__( self ):
        self._weightlist = [ 2.0, 0.8, -0.5 ] # per idxInpt
#        self._ylist = [] # per value set

        ## training set
        ##
        ## target
        ## bias
        ## x1
        ## x2
        self._trainingset2 = [ [1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  1.0,  1.0,  1.0,  1.0,  1.0]
                              ,[1.0, 6.0, 3.0, 4.0, 3.0, 1.0,  6.0,  7.0,  6.0, 10.0,  4.0]
                              ,[8.0, 2.0, 6.0, 4.0, 1.0, 6.0, 10.0,  7.0, 11.0,  5.0, 11.0] ]

        self._targetlist2 = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
        self._learningrate = 1.0/50.0
        self._epochdwlist = [ [self._weightlist[0]], [self._weightlist[1]], [self._weightlist[2]] ]
        self._epochtime = [0]

    def snapshot( self ):
        ## class data: dots
        class1x = self._trainingset2[1][:6]
        class1y = self._trainingset2[2][:6]
        plt.plot( class1x, class1y, 'ro' )
        class2x = self._trainingset2[1][6:]
        class2y = self._trainingset2[2][6:]
        plt.plot( class2x, class2y, 'bo' )

        xAxisMax = max(class1x + class2x)+1
        xAxisMin = min(class1x + class2x)-1
        yAxisMax = max(class1y + class2y)+1
        yAxisMin = min(class1y + class2y)-1
        plt.axis( [xAxisMin, xAxisMax, yAxisMin, yAxisMax] )

        ## separation line
        w0 = self._weightlist[0]
        w1 = self._weightlist[1]
        w2 = self._weightlist[2]

        x1 = -20.0
        y1 = (-w0 -x1*w1) / w2
        x2 = 20.0
        y2 = (-w0 -x2*w1) / w2
        plt.plot( [x1, x2], [y1, y2] )

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.show()

    def snapshot_learning( self ):
        ## print weightlist
        plt.plot( self._epochtime, self._epochdwlist[0] )
        plt.plot( self._epochtime, self._epochdwlist[1] )
        plt.plot( self._epochtime, self._epochdwlist[2] )
        plt.xlabel('time')
        plt.ylabel('error')
        plt.show()

    def training( self ):
## calculating net epochs
        for epoch in range(0, 200):
            dwlist = [0,0,0] # per value, since then averaged

## forward pass (linear)
            intermediate = []
            total = 0
            for idxVal in range(0, len(self._trainingset2[0])):
                y = 0
                total += 1
                for idxInpt in range(0, len(self._trainingset2)):
                    inpt = self._trainingset2[idxInpt]
                    weight = self._weightlist[idxInpt]
                    xval = inpt[idxVal]
                    ## sum of values
                    y += xval * weight

## accumulate dw
                for idxInpt in range(0, len(self._trainingset2)): #  per input data
                    inpt = self._trainingset2[idxInpt]
                    xval = inpt[idxVal]
                    target = self._targetlist2[idxVal]
                    ## sum of dw
                    dwlist[idxInpt] += (target - y) * xval

## average dw per input
            for idxDw in range(0, len(dwlist)):
                dwlist[idxDw] = dwlist[idxDw] / total

                ## collect data over epochs for plotting
                self._epochdwlist[idxDw].append(dwlist[idxDw])
            ## time for plotting
            self._epochtime.append( epoch )

## plotting
            if 0 == epoch: self.snapshot()
            if 1 == epoch: self.snapshot()

## apply dw and learning rate
            for idxWeight in range(0, len(self._weightlist)):
                self._weightlist[idxWeight] += self._learningrate * dwlist[idxWeight]


if __name__ == '__main__':
    nn = Perceptron()
    nn.training()
    nn.snapshot()
    nn.snapshot_learning()

print "READY."
