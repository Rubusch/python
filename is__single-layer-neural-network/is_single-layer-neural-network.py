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
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )



weightlist = [ 2.0, 0.8, -0.5 ] # per idxInpt



ylist = [] # per value set

 
# targetlist = [ 1.0, -1.0 ] # per idxClss

# trainingsset = []

# bias = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
# x1   = [1.0, 6.0, 3.0, 4.0, 3.0, 1.0]
# x2   = [8.0, 2.0, 6.0, 4.0, 1.0, 6.0]
# trainingsset.append([bias, x1, x2])
# bias = [ 1.0, 1.0,  1.0,  1.0,  1.0]
# x1   = [ 6.0, 7.0,  6.0, 10.0,  4.0]
# x2   = [10.0, 7.0, 11.0,  5.0, 11.0]
# trainingsset.append([bias, x1, x2])
 


## training set
##
## target
## bias
## x1
## x2
trainingset2 = [ [1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  1.0,  1.0,  1.0,  1.0,  1.0]
                ,[1.0, 6.0, 3.0, 4.0, 3.0, 1.0,  6.0,  7.0,  6.0, 10.0,  4.0]
                ,[8.0, 2.0, 6.0, 4.0, 1.0, 6.0, 10.0,  7.0, 11.0,  5.0, 11.0] ]

targetlist2 = [ 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
 

learningrate = 1.0/50.0

epochdwlist = [ [weightlist[0]], [weightlist[1]], [weightlist[2]] ]
epochtime = [0]

def snapshot():
    print weightlist  

    ## class data: dots

    # class1x = trainingsset[0][1]
    # class1y = trainingsset[0][2]
    # plt.plot( class1x, class1y, 'ro' )
    # class2x = trainingsset[1][1]
    # class2y = trainingsset[1][2]
    # plt.plot( class2x, class2y, 'bo' )

    class1x = trainingset2[1][:6]
    class1y = trainingset2[2][:6]
    plt.plot( class1x, class1y, 'ro' )
    class2x = trainingset2[1][6:]
    class2y = trainingset2[2][6:]
    plt.plot( class2x, class2y, 'bo' )


    xAxisMax = max(class1x + class2x)+1
    xAxisMin = min(class1x + class2x)-1
    yAxisMax = max(class1y + class2y)+1
    yAxisMin = min(class1y + class2y)-1
    plt.axis( [xAxisMin, xAxisMax, yAxisMin, yAxisMax] )

    ## separation line
    w0 = weightlist[0]
    w1 = weightlist[1]
    w2 = weightlist[2]

    x1 = -20.0
    y1 = (-w0 -x1*w1) / w2
    x2 = 20.0
    y2 = (-w0 -x2*w1) / w2
    plt.plot( [x1, x2], [y1, y2] )

    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()



## calculating net epochs
for epoch in range(0, 2500):
    dwlist = [0,0,0] # per value, since then averaged

## forward pass (linear)
    intermediate = []
    total = 0
#    for idxClss in range(0, len(trainingsset)): # per class
#        clss = trainingsset[idxClss]
#        target = targetlist[idxClss]
#        inpt = clss[0]
#        for idxVal in range(0, len(inpt)): # per value in input data
    for idxVal in range(0, len(trainingset2[0])):
        y = 0
        total += 1
        for idxInpt in range(0, len(trainingset2)):
#        for idxInpt in range(0, len(clss)): #  per input data
#            inpt = clss[idxInpt]
            inpt = trainingset2[idxInpt]
            weight = weightlist[idxInpt]
            xval = inpt[idxVal]
            ## sum of values
            y += xval * weight

## accumulate dw
        for idxInpt in range(0, len(trainingset2)): #  per input data
            inpt = trainingset2[idxInpt]
            xval = inpt[idxVal]
            target = targetlist2[idxVal]
            ## sum of dw
            dwlist[idxInpt] += (target - y) * xval


## average dw per input
    for idxDw in range(0, len(dwlist)):
        dwlist[idxDw] = dwlist[idxDw] / total

        ## collect data over epochs
        epochdwlist[idxDw].append(dwlist[idxDw])
    epochtime.append( epoch )

## plot data
    if 0 == epoch: snapshot()

## apply dw and learning rate
    for idxWeight in range(0, len(weightlist)):
        weightlist[idxWeight] += learningrate * dwlist[idxWeight]

## print weightlist
# plt.plot( epochtime, epochdwlist[0] )
# plt.plot( epochtime, epochdwlist[1] )
# plt.plot( epochtime, epochdwlist[2] )
# plt.xlabel('time')
# plt.ylabel('error')
# plt.show()

snapshot()
                                                                                        
# FIXME: separation line misses 2 points

print "READY."
