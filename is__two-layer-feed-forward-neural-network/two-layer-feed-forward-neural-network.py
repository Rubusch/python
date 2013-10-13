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
#from math import exp
import math



def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )

class Perceptron( object ):
    ## overview
    _weight1list = []  # weights, 1st layer 
    _weight2list = []  # weights, second layer 

    _weight1matrix = [] # weights, 1st thru 2nd layer
    _weight2matrix = [] # weights, 2nd thru net layer
    _dwhistory = []     # printable history of dw
    _hiddendata = []    # hidden data

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

        
        # self._trainingset      =  [[1.0, 1.0, 1.0, 1.0, 1.0,    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        #                           ,[4.0, 4.0, 5.0, 5.0, 7.0,    1.0, 2.0, 3.0, 6.0, 3.0, 6.0, 4.0, 7.0]
        #                           ,[2.0, 4.0, 3.0, 1.0, 2.0,    2.0, 1.0, 1.0, 5.0, 6.0, 7.0, 6.0, 6.0]]

        
        self._trainingdata = [ [1.0, 4.0, 2.0]
                             , [1.0, 4.0, 4.0]
                             , [1.0, 5.0, 3.0]
                             , [1.0, 5.0, 1.0]
                             , [1.0, 7.0, 2.0]
                             , [1.0, 1.0, 2.0]
                             , [1.0, 2.0, 1.0]
                             , [1.0, 3.0, 1.0]
                             , [1.0, 6.0, 5.0]
                             , [1.0, 3.0, 6.0]
                             , [1.0, 6.0, 7.0]
                             , [1.0, 4.0, 6.0]
                             , [1.0, 7.0, 6.0] ]

        
        # self._trainingtargetlist = [1.0, 1.0, 1.0, 1.0, 1.0,   -1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0]
        
        self._trainingtargetdata = [[1.0]
                                   ,[1.0]
                                   ,[1.0]
                                   ,[1.0]
                                   ,[1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]
                                   ,[-1.0]]

# TODO
        self._testset          = [ [1.0, 1.0, 1.0, 1.0, 1.0, 1.0,    1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                                  ,[4.0, 5.0, 3.0, 5.0, 6.0, 7.0,    3.0, 8.0, 4.0, 7.0, 2.0, 2.0]
                                  ,[1.0, 2.0, 4.0, 4.0, 1.0, 1.0,    2.0, 7.0, 7.0, 5.0, 3.0, 5.0]]

# TODO
        self._testtargetlist     = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0,   -1.0,-1.0,-1.0,-1.0,-1.0,-1.0]

        
        # self._hiddenlist       =  [[1.0, 1.0, 1.0, 1.0, 1.0,    1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] 
        #                           ,[0.0, 0.0, 0.0, 0.0, 0.0,    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        
        self._hiddendata = [[0.0, 0.0, 0.0]]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]
                          # , [1.0, 0.0, 0.0, 0.0]]

        
#         ## 1-layer weights
#         nnset = self._trainingset  
# #        for idxWeight in range( 0, 3 * len( nnset )): 
#         for idxWeight in range( 0, (len(self._hiddenlist) -1) * len( nnset )): 
#             self._weight1list.append( random.randrange(-100, 100) / 1000.0 )
# #        self._weight1list = [1,1,1,1,1,1,1,1,1] ## debugging        
        
        ## 1. layer weights
#        nhidden = len(self._hiddendata[0])-1 # w/o bias
        nhidden = len(self._hiddendata[0])
        ninput = len(self._trainingdata[0])
        self._weight1matrix = self._initweights( ninput, nhidden)

            
#        ## 2-layer weights
#        nnset = self._hiddenlist  
#        for idxWeight in range( 0, len( nnset )):
#            self._weight2list.append( random.randrange(-100, 100) / 1000.0 )
##        self._weight2list = [1,1,1,1] ## debugging        
            
        ## 2. layer weights
        nhidden = len(self._hiddendata[0])
        ny = 1
        self._weight2matrix = self._initweights( nhidden, ny)

        ## learningrate nu
        ## 1.0, 1.0/3.0, 1.0/10.0, 1.0/30.0, 1.0/100.0, 1.0/300.0, 1.0/1000.0
#        self._learningrate = 1.0
#        self._learningrate = 1.0/3.0
#        self._learningrate = 1.0/10.0
        self._learningrate = 1.0/30.0
#        self._learningrate = 1.0/100.0
#        self._learningrate = 1.0/300.0
#        self._learningrate = 1.0/1000.0

        
#        for idxHidden in range(0, len(self._trainingset) * (len(self._hiddenlist)-1) + len(self._hiddenlist)):
#            self._epochdwlist.append([0.0])
#        self._epochtime = [0]
        
        ## history per weight entry
        self._dwhistory = []

        for y in range(0, len(self._weight1matrix)):
            for x in range(0, len(self._weight1matrix[0])):
                self._dwhistory.append( [self._weight1matrix[y][x]] )

        for y in range(0, len(self._weight2matrix)):
            for x in range(0, len(self._weight2matrix[0])):
                self._dwhistory.append( [self._weight2matrix[y][x]] )


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

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.show()


    def snapshot_learning( self ):
#         for idx in range(0, len(self._epochdwlist)):
#             if ((len(self._hiddenlist)-1)*len(self._trainingset)) == idx: continue
#             if ((len(self._hiddenlist)-1)*(len(self._hiddenlist)-1)) == idx: continue

# #            print "plot " + str(idx) ## debugging 
#             plt.plot( self._epochdwlist[idx] )
# #            plt.show() ## debugging 
        for idx in range(0, len(self._dwhistory)):
#            print "plot " + str(idx) ## debugging 
            plt.plot( self._dwhistory[idx] )
#            plt.show() ## debugging 


        plt.xlabel('time')
        plt.ylabel('error')
        plt.show()


    def _initweights( self, nsource, ntarget):
        weightmatrix = []
        for h in range(0, nsource):
            tmp = []
            for x in range(0, ntarget):
                tmp += [random.randrange(-100, 100) / 1000.0]
            weightmatrix.append(tmp)
        return weightmatrix


    def sigma( self, mat ):
        print ""
        self.mat_show( mat )
        print "sigma"
        res = []
        for y in range(0, len(mat)):
            tmp = []
            for x in range(0, len(mat[0])):
                tmp += [1/(1 + math.exp(mat[y][x]))]
            res.append(tmp)

        self.mat_show( res )
        return res

    def revsigma( self, mat ):
        ## revsigma = sigma(x) * (1 - sigma(x))
        sigmat = self.sigma(mat)

        ## sigma*sigma
        res = []
        for y in range(0,len(sigmat)):
            tmp = []
            for x in range(0, len(sigmat[0])):
                tmp += [sigmat[y][x] * sigmat[y][x]]
            res.append(tmp)

        ## -(sigma*sigma)
        res = self.mat_factorize( -1, res )

        ## sigma - (sigma*sigma) == sigma * (1 - sigma)
        return self.mat_addition( sigmat, res )

    def mat_multiplication( self, a, b ):
        print ""
        self.mat_show( a )
        print "x"
        self.mat_show( b )

        aylen = len( a )
        axlen = len( a[0] )

        bylen = len( b )
        bxlen = len( b[0] )

        ## safety
        if axlen != bylen: die("matrix multiplication: nonconformat arguments")

        cylen = aylen
        cxlen = bxlen

        ## init c
        c = []
        for y in range(0, cylen):
            row = []
            for x in range(0, cxlen):
                row += [0]
            c.append( row )

        ## matrix matrix multiplication, brute force
        for ay in range(0,aylen):

            for bx in range(0,bxlen):
                tmp = 0
                for xy in range(0,bylen):
                    tmp += a[ay][xy] * b[xy][bx]
                c[ay][bx] = tmp

        print "="
        self.mat_show( c )

        return c

    def mat_transpose( self, mat ):
        print ""
        self.mat_show( mat ) 
        print "transpose"
        trans = []
        for y in range(0, len(mat[0])):
            tmp = []
            for x in range(0, len(mat)):
                tmp += [mat[x][y]]
            trans.append(tmp)
        self.mat_show( trans ) 
        return trans

    def mat_addx( self, a, b ):
        print ""
        self.mat_show( a ) 
        print "addx"
        self.mat_show( b ) 
        if len(a) != len(b): die("mat_addx failed, different sizes")
        c = []
        for y in range(0,len(a)):
            c.append( a[y] + b[y] )
        print "="
        self.mat_show( c ) 
        return c

    def mat_addy( self, a, b ):
        print ""
        self.mat_show( a ) 
        print "addy"
        self.mat_show( b ) 
        if len(a[0]) != len(b[0]): die("mat_addy failed: different sizes")
        c = [i for i in a]
        c += [i for i in b]
        print "="
        self.mat_show( c ) 
        return c

    def mat_addition( self, a, b ):
        print ""
        self.mat_show( a ) 
        print "addition"
        self.mat_show( b ) 
        if len(a) != len(b): die("mat_addition failed: not implemented for different sizes")
        c = []
        for y in range(0, len(a)):
            tmp = []
            for x in range(0, len(a[0])):
                tmp += [a[y][x] + b[y][x]]
            c.append(tmp)
        print "="
        self.mat_show( c ) 
        return c

    def mat_factorize( self, fact, mat ):
        print ""
        print fact
        print "*"
        self.mat_show( mat )
        res = []
        for y in range(0, len(mat)):
            tmp = []
            for x in range(0, len(mat[0])):
                tmp += [fact * mat[y][x]]
            res.append( tmp )
        print "="
        self.mat_show( res ) 
        return res

    def mat_avg( self, old, new):
        print ""
        self.mat_show( old ) 
        print "avg"
        self.mat_show( new ) 
        if 0 == len(old): return [i for i in new]
        res = []
        for y in range(0,len(new)):
            tmp = []
            for x in range(0,len(new[0])):
                tmp += [ (old[y][x] + new[y][x]) / 2 ]
            res.append(tmp)
        print "="
        self.mat_show( res ) 
        return res

    def mat_show( self, mat ):
        for y in range(0,len(mat)):
            for x in range(0,len(mat[y])):
                print mat[y][x],
            print ""

    def update_history( self ):
        # print "hist"
        # print self._dwhistory 
        # print "mat1"
        # print self._weight1matrix
        # print "mat2"
        # print self._weight2matrix

#        print self._dwhistory  
        idx = 0
        for y in range(0, len(self._weight1matrix)):
            for x in range(0, len(self._weight1matrix[0])):
                self._dwhistory[idx] += [self._weight1matrix[y][x]]
                idx +=1
#                self._dwhistory.append( [self._weight1matrix[y][x]] )

        for y in range(0, len(self._weight2matrix)):
            for x in range(0, len(self._weight2matrix[0])):
                self._dwhistory[idx] += [self._weight2matrix[y][x]]
                idx +=1
#                self._dwhistory.append( [self._weight2matrix[y][x]] )

#        print self._dwhistory
#        die( "XXX" )


    def training( self ):
## init, no bias in dwlist1 connections
        
#        currentset = self._trainingset
#        currenttargetlist = self._trainingtargetlist
        
        current_data = self._trainingdata
        current_targetdata = self._trainingtargetdata

        
        # dwlist1 = []
        # dwlist2 = []
        # for idxHidden in range(0, len(currentset) * (len(self._hiddenlist)-1)):
        #     dwlist1.append(0.0)
        # for idxHidden in range(0, len(self._hiddenlist)):
        #     dwlist2.append(0.0)
            
        dw1data = []
        for y in self._weight1matrix:
            tmp=[]
            for x in self._weight1matrix[0]:
                tmp += [0.0]
            dw1data.append(tmp)
        dw1data_history = []

        dw2data = []
        for y in self._weight2matrix[0]: # TODO check this
            tmp = []
            for x in self._weight2matrix:
                tmp += [0.0]
            dw2data.append( tmp )
        dw2data_history = []


## calculating net epochs
#        maxtime = 1000
        maxtime = 100
        for epoch in range(0, maxtime):

# TODO         
#            if (maxtime-1) == epoch:
#                currentset = self._testset
#                currenttargetlist = self._testtargetlist

            dw = 0
            total = 0

## forward pass (linear)
            y = 0
#            for idxVal in range(0, len(currentset[0])): # per value set, 13x
            for idxVal in range(0, len(current_data)):
                current_input = [current_data[idxVal]]
                total += 1

## forward - layer 1
                
#                 for idxInpt in range(0, len(currentset)): # per input node + bias, here 3x
#                     inpt = currentset[idxInpt]
#                     xval = inpt[idxVal]
#                     for idxHidden in range(1, len(self._hiddenlist)): # per hidden node, 1 = no bias
# #                        idxWeight = 3* idxInpt + (idxHidden-1)
#                         idxWeight = (len(self._hiddenlist) -1) * idxInpt + (idxHidden-1)
#                         weight = self._weight1list[idxWeight]
#                         ## sum of values
#                         self._hiddenlist[idxHidden][idxVal] += self.sigma(xval * weight)
#                     ## / idxHidden
#                 ## / idxInpt
                
                # input * weights
                self._hiddendata = self.mat_multiplication( current_input, self._weight1matrix)
                # sigma
                self._hiddendata = self.sigma( self._hiddendata )

## forward - layer 2
                
                # y = 0
                # for idxHidden in range(0, len(self._hiddenlist)): # per hidden node, 3 + 1 (bias)
                #     hidden = self._hiddenlist[idxHidden][idxVal]
                #     weight = self._weight2list[idxHidden]
                #     ## propagation
                #     y += hidden * weight
                # ## / idxHidden
                    
                net = self.mat_multiplication( self._hiddendata, self._weight2matrix ) 

## preparing dw from sum(y)
                
#                target = currenttargetlist[idxVal]
                

## backward pass - layer 2
                
#                 ## dwlist2 = nu * y[j] * delta = nu * y[j] * (y[k] - t) * dy/dnet
#                 dwtmp2 = [] # just to transfer to next block (as backup)
#                 for idxHidden in range(0, len( self._hiddenlist) ): # per hidden node, 3 + 1 (bias)
#                     hidden =  self._hiddenlist[idxHidden]
#                     xval = hidden[idxVal]
#                     ## backward: learningrate * delta * outputvalue
#                     dwtmp2.append(self._learningrate * (target - y) * xval)
# ## DEBUG some checks where original settings seem to explode in infinity, and finally NAN values
#                     if math.isnan(dwlist2[idxHidden]): die( "NAN" )   
#                     if math.isinf(dwlist2[idxHidden]): die( "INF" )   
#                     dwlist2[idxHidden] += self._learningrate * (target-y) * xval # backup
#                 ## / idxHidden
                    


                ## backward: learningrate * delta * outputvalue
                dw = current_targetdata[idxVal][0] - net[0][0]
                dw *= self._learningrate 
                dw2data = self.mat_factorize( dw, self._hiddendata )#* outputvalue


                ## dwlist1 = nu * x * delta = nu * x * dwlist2, per x neuron
                        
#                 dwtmp1 = []
#                 for idxInpt in range(0, len(currentset)): # per input node + bias, here 3x
#                     inpt = currentset[idxInpt]
#                     xval = inpt[idxVal]
#                     for idxHidden in range(1, len( self._hiddenlist) ): # per hidden node, 3 + 1 (bias)
# #                        idxWeight = 3* idxInpt + (idxHidden-1)
#                         idxWeight = (len(self._hiddenlist) -1) * idxInpt + (idxHidden-1)   
#                         ## backward: 
#                         dwlist1[idxWeight] += self._learningrate * xval * dwtmp2[idxHidden]
#                     ## / idxHidden
#                 ## / idxInpt
                        
                dw1tmp = self.revsigma( dw2data )
                dw1tmp = self.mat_factorize( self._learningrate, dw1tmp ) 

#                dw1tmp = self.mat_multiplication( dw1tmp, self._weight1matrix) # TODO is this a matrix multiplication?
                tr_weight1matrix = self.mat_transpose( self._weight1matrix ) # TODO check
                dw1tmp = self.mat_multiplication( dw1tmp, tr_weight1matrix) # TODO is this a matrix multiplication?
                
#                self.mat_show( current_input ) # input, x

#                dw1tmp = self.mat_addy( self.mat_addy( dw1tmp, dw1tmp), dw1tmp)
                dw1next = self.mat_addy( dw1tmp, dw1tmp)
                dw1next = self.mat_addy( dw1next, dw1tmp )
                dw1data = self.mat_addition( dw1data, dw1next )



#                for y in range(0, len(self._hiddendata)):
#                    for x in range(0, len(self._hiddendata[0])):
#                        dw2data[y][x] += self._learningrate * 
#                dw1data[y][x] += self._learningrate * self.revsigma(self._hiddenlist - bias)
#                idxWeight = (len(self._hiddenlist) -1) * self.revsigma( idxInpt + (idxHidden-1))   

                
#                print "---"
#                self.mat_show( dw1data ) 
#                self.mat_show( dw2data ) 

                dw1data_history = self.mat_avg( dw1data_history, dw1data)
                dw2data_history = self.mat_avg( dw2data_history, dw2data)


#                print "---"
#                self.mat_show( dw1tmp )
#
            ## / idxVal

## average dw
#             for idxDw in range(0, len(dwlist1)):
#                 dwlist1[idxDw] = dwlist1[idxDw] / total    
# #                dwlist1[idxDw] = dwlist1[idxDw] / (total*total) ## QUICKFIX: to average it down, I square the totals
#             ## / idxInpt

#             for idxHidden in range(0, len(dwlist2)):
#                 dwlist2[idxHidden] = dwlist2[idxHidden] / total    
# #                dwlist2[idxHidden] = dwlist2[idxHidden] / (total*total) ## QUICKFIX: to average it down, I square the totals
#             ## / idxHidden

                
# ## apply de-averaged dw's to the corresponding weights
#             idxEpochplot = 0
#             for idxWeight in range(0, len(self._weight1list)):
# #                 self._weight1list[idxWeight] += dwlist1[idxWeight]     
#                 self._weight1list[idxWeight] = dwlist1[idxWeight] ## QUICKFIX: assign rather than do: w(new) = dw + w(old)
#                 self._epochdwlist[idxWeight].append(self._weight1list[idxWeight])
#                 dwlist1[idxWeight]=0.0
#                 idxEpochplot += 1

#             for idxWeight in range(0, len(self._weight2list)):
# #                 self._weight2list[idxWeight] += dwlist2[idxWeight]     
#                 self._weight2list[idxWeight] = dwlist2[idxWeight] ## QUICKFIX: assign rather than do: w(new) = dw + w(old)
#                 self._epochdwlist[idxEpochplot+idxWeight].append(self._weight2list[idxWeight])
#                 dwlist2[idxWeight]=0.0
                
            self._weight1matrix = self.mat_addition( self._weight1matrix, dw1data_history )
            self._weight2matrix = self.mat_addition( self._weight2matrix, self.mat_transpose(  dw2data_history) )

            self.update_history()
            
            print "---"
            self.mat_show( self._dwhistory )   
#            if 3 == epoch: die("XXX")
        ## / epoch
        ## dw = nu * y * (y-t) d/dnet


if __name__ == '__main__':
     nn = Perceptron()

## test
     ## matrices
#     a = [[1.0,1.0,1.0],[2.0,2.0,2.0],[3.0,3.0,3.0]]
#     a = [[1,1,1],[2,2,2]]
#     a = [[1],[1],[1]]
#     b = [[1.0,2.0,3.0], [1.0,2.0,3.0], [1.0,2.0,3.0]]

#     nn.mat_show( a ) 
#     print ""
#     nn.mat_show( b ) 
#     print ""

     ## matrix matrix multiplication
#     c = nn.mat_multiplication( a, b )
#     nn.mat_show( c )

     ## dot product
#     nn.mat_transpose(a)
#     nn.mat_addx( a, b )
#     nn.mat_addy( a, b )
#     nn.mat_addition( a, b )
#     nn.mat_factorize( 4, b )
#     print ""
#     res = nn.revsigma( a )
#     print "---"
#     nn.mat_show( res )

#     nn.mat_avg( [], b)
#     nn.mat_avg( a, b)
#     die( "STOP" )
    
#     nn.snapshot()
     nn.training()  
#     nn.snapshot()
     nn.snapshot_learning()

print "READY."
