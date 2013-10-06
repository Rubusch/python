#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Code to train a single-layer neural network
# Assignment01 for Intelligent Systems
#

# (60+5 points total) Write code to train the two-layer feed-forward neural network
# with the architecture depicted in fig 2.

# The training set consists of the following data points:
#   Class 1 (t = 1): (4,2), (4,4), (5,3), (5,1), (7,2)
#   Class 2 (t = -1): (1,2), (2,1), (3,1), (6,5), (3,6), (6,7), (4,6), (7,6)
# The accompanying test set is:
#   Class 1 (t = 1): (4,1), (5,2), (3,4), (5,4), (6,1), (7,1)
#   Class 2 (t = -1): (3,2), (8,7), (4,7), (7,5), (2,3), (2,5)
# This network uses sigmoidal activation function (i.e. the logistic function) for the
# hidden layer and linear activation for the output layer. Also, don't forget the biases
# (even though they are not shown in the image). The weights (and biases) should
# be randomly initialized from a uniform distribution in the range [-0.1, 0.1].
# (a) (5 points) Plot the data. Would the network be able to solve this task if it
# had linear neurons only? Explain why.
# (b) (30 points) Implement and apply backpropagation (with nu = 1/30) until all
# examples are correctly classified. (This might take a few thousand epochs)
# (c) (10 points) Perform 10 runs with different random initializations of the weights,
# and plot the training and test error for each epoch averaged across the 10
# runs. How many epochs does it take, on average, to correctly classify all
# points. What do you notice?
# (d) (15 points) Try different learning rates nu = [1, 1/3, 1/10, 1/30, 1/100, 1/300, 1/1000]
# and plot the training error over 1000 epochs. What is the effect of varying
# the learning rate?
# (e) (Bonus: 5 points) Vary the number of hidden units (from 1 to 10) and run
# each network with 10 different random initializations. Plot the average train
# and test errors. Explain the effect of varying the number of hidden units.
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

## exponent, e.g. e**val
from math import exp



def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )

class Perceptron( object ):
    ## overview
    _weight1list = []  # weights, 1st layer
    _weight2list = []  # weights, second layer
    _trainingset = []  # training data (class 1 and 2)
    _testset = []      # test set
    _trainingtargetlist = []   # targets (size of class 1 + 2)
    _hiddenlist = []   # hidden nodes
    _learningrate = [] # provided
    _epochdwlist = []  # for plotting
    _epochtime = []    # for plotting

    def __init__( self ):
        ## training set
        ##
        ## target
        ## bias
        ## x1
        ## x2
        self._trainingset      =  [[1.0, 1.0, 1.0, 1.0, 1.0,    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                                  ,[4.0, 4.0, 5.0, 5.0, 7.0,    1.0, 2.0, 3.0, 6.0, 3.0, 6.0, 4.0, 7.0]
                                  ,[2.0, 4.0, 3.0, 1.0, 2.0,    2.0, 1.0, 1.0, 5.0, 6.0, 7.0, 6.0, 6.0]]

        self._hiddenlist       =  [[1.0, 1.0, 1.0, 1.0, 1.0,    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                                  ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                                  ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                                  ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        self._trainingtargetlist = [1.0, 1.0, 1.0, 1.0, 1.0,   -1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]

        self._testset          = [ [1.0, 1.0, 1.0, 1.0, 1.0, 1.0,    1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                                  ,[4.0, 5.0, 3.0, 5.0, 6.0, 7.0,    3.0, 8.0, 4.0, 7.0, 2.0, 2.0]
                                  ,[1.0, 2.0, 4.0, 4.0, 1.0, 1.0,    2.0, 7.0, 7.0, 5.0, 3.0, 5.0]]
        self._testtargetlist     = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0,   -1.0,-1.0,-1.0,-1.0,-1.0,-1.0]

        ## 1-layer weights
        nnset = self._trainingset  
#        for idxWeight in range( 0, 3 * len( nnset )):
#            self._weight1list.append( random.randrange(-100, 100) / 1000.0 )
        self._weight1list = [1,1,1,1,1,1,1,1,1]         

        ## 2-layer weights
#        for idxWeight in range( 0, 1 + len( nnset )):
#            self._weight2list.append( random.randrange(-100, 100) / 1000.0 )
        self._weight2list = [1,1,1,1]         

        ## learningrate nu
        self._learningrate = 1.0/30.0
#        self._epochdwlist = [ [self._weightlist[0]], [self._weightlist[1]], [self._weightlist[2]] ] 
#        self._epochtime = [0]

    def snapshot( self ):
        ## class data: dots
        class1x = self._trainingset[1][:6]
        class1y = self._trainingset[2][:6]
        plt.plot( class1x, class1y, 'ro' )
        class2x = self._trainingset[1][6:]
        class2y = self._trainingset[2][6:]
        plt.plot( class2x, class2y, 'bo' )

        xAxisMax = max(class1x + class2x)+1
        xAxisMin = min(class1x + class2x)-1
        yAxisMax = max(class1y + class2y)+1
        yAxisMin = min(class1y + class2y)-1
        plt.axis( [xAxisMin, xAxisMax, yAxisMin, yAxisMax] )

# TODO no separation line
        # ## separation line
        # w0 = self._weightlist[0]
        # w1 = self._weightlist[1]
        # w2 = self._weightlist[2]

        # x1 = -20.0
        # y1 = (-w0 -x1*w1) / w2
        # x2 = 20.0
        # y2 = (-w0 -x2*w1) / w2
        # plt.plot( [x1, x2], [y1, y2] )

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.show()

    def snapshot_learning( self ):
        plt.plot( self._epochtime, self._epochdwlist[0] )
        plt.plot( self._epochtime, self._epochdwlist[1] )
        plt.plot( self._epochtime, self._epochdwlist[2] )
        plt.xlabel('time')
        plt.ylabel('error')
        plt.show()

    def sigma( self, product ):
        return 1/(1 + exp(product))

    def training( self ):
        dwlist2 = []
        for idxHidden in range(0, len(self._hiddenlist)):
            dwlist2.append(0.0)

## calculating net epochs
        for epoch in range(0, 200):
            dwlist1 = [0,0,0] # per value, since then averaged
            for idxHidden in range(0, len(self._hiddenlist)):
                dwlist2[idxHidden] = 0.0
            dw = 0
            total = 0
## forward pass (linear)
            y = 0
            for idxVal in range(0, len(self._trainingset[0])): # per value, 13x
                total += 1

## forward - layer 1
                for idxInpt in range(0, len(self._trainingset)): # per input node + bias, here 3x
                    inpt = self._trainingset[idxInpt]
                    xval = inpt[idxVal]
                    for idxHidden in range(1, len(self._hiddenlist)): # per hidden node, 1 = no bias
                        idxWeight = 3* idxInpt + (idxHidden-1)
                        weight = self._weight1list[idxWeight]
                        ## sum of values
                        self._hiddenlist[idxHidden][idxVal] += self.sigma(xval * weight)
                    ## / idxHidden
                ## / idxInpt

                        
                # print self._hiddenlist[0]  
                # print self._hiddenlist[1]  
                # print self._hiddenlist[2]  
                # print self._hiddenlist[3]  
                        

## forward - layer 2
                y = 0
                for idxHidden in range(0, len(self._hiddenlist)): # per hidden node, 3 + 1 (bias)
                    hidden = self._hiddenlist[idxHidden][idxVal]
                    weight = self._weight2list[idxHidden]
                    y += hidden * weight
                ## / idxHidden

## preparing dw from sum(y)
                target = self._trainingtargetlist[idxVal]
                dw = y - target

## backward pass - layer 2
                ## dwlist2 = nu * y[j] * delta = nu * y[j] * (y[k] - t) * dy/dnet
                dwtmp2 = [] # just to transfer to next block (as backup)
                for idxHidden in range(0, len( self._hiddenlist) ): # per hidden node, 3 + 1 (bias)
                    hidden =  self._hiddenlist[idxHidden]
                    dwtmp2.append(self._learningrate * dw * hidden[idxVal])
                    dwlist2[idxHidden] += self._learningrate * dw * hidden[idxVal]
                ## / idxHidden

                ## dwlist1 = nu * x * delta = nu * x * dwlist2, per x neuron
                dwtmp1 = []
                for idxInpt in range(0, len(self._trainingset)): # per input node + bias, here 3x
                    inpt = self._trainingset[idxInpt]
                    xval = inpt[idxVal]
                    for idxHidden in range(1, len( self._hiddenlist) ): # per hidden node, 3 + 1 (bias)
                        dwlist1[idxInpt] += self._learningrate * xval * dwtmp2[idxHidden]
                    ## / idxHidden
                ## / idxInpt
            ## / idxVal

## average dw
            for idxInpt in range(0, len(self._trainingset)): # per input node + bias, here 3x
                dwlist1[idxInpt] = dwlist1[idxInpt] / total
            ## / idxInpt

            for idxHidden in range(0, len(dwlist2)):
                dwlist2[idxHidden] = dwlist2[idxHidden] / total
            ## / idxHidden


## apply de-averaged dw's to the corresponding weights
        die(dwList2)  

        for idxWeight in range(0, len(self._weight1list)):
            self._weight1List[idxWeight] = dwlist1[idxWeight]

        for idxWeight in range(0, len(self._weight2list)):
            self._weight2List[idxWeight] = dwlist2[idxWeight]

        ## / epoch

            print dwlist1  
            die( "STOP" )  

## dw = nu * y * (y-t) d/dnet                    






# ## accumulate dw
#                 for idxInpt in range(0, len(self._trainingset)): #  per input data
#                     inpt = self._trainingset[idxInpt]
#                     xval = inpt[idxVal]
#                     target = self._trainingtargetlist[idxVal]
#                     ## sum of dw
#                     dwlist[idxInpt] += (target - y) * xval

# ## average dw per input
#             for idxDw in range(0, len(dwlist)):
#                 dwlist[idxDw] = dwlist[idxDw] / total

#                 ## collect data over epochs for plotting
#                 self._epochdwlist[idxDw].append(dwlist[idxDw])
#             ## time for plotting
#             self._epochtime.append( epoch )

## plotting
#            if 0 == epoch: self.snapshot()
#            if 1 == epoch: self.snapshot()

## apply dw and learning rate
#            for idxWeight in range(0, len(self._weightlist)): 
#                self._weightlist[idxWeight] += self._learningrate * dwlist[idxWeight] 

        die("END OF LOOOP")         
                      


if __name__ == '__main__':
    nn = Perceptron()
#    nn.snapshot()
    nn.training()
#    nn.snapshot()
#    nn.snapshot_learning()

print "READY."
