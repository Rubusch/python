#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

#import math
from math import *
import sys

XMAX=6
YMAX=4

## fcn distance
def distance( pktsrc, pktdst ):
    dist = 0
#    dists=[]
#    try:
#        for elem in pktdst[:]:
#            dy = pktsrc[0] - elem[0]
#            dx = pktsrc[1] - elem[1]
#            dists += [sqrt(dx^2 + dy^2)]
#            dist = min(dists[:])
#    except TypeError:
    dy = pktsrc[0] - pktdst[0]
    dx = pktsrc[1] - pktdst[1]
    dist = sqrt(dx^2 + dy^2)
    return dist

## normalize
def normalize( M ):
    maxvals = []
    maxval = -1
    ## find overall max
    for y in range( len(M) ):
        maxvals += [max([elem for elem in M[y]])]
    maxval = max( maxvals[:] )
    ## divide each value by overall max
    for y in range( len(M) ):
        for x in range( len(M[0]) ):
            M[y][x] = M[y][x] / maxval
    return M

## fcn obstacle
def obstacle( M ):
    # TODO
    return M

## fcn repulsive_potential_field
def repulsive_potential_field( M ):
    # TODO
    return M

## fcn attractive_potential_field
def attractive_potential_field( M ):
    # TODO
    return M

## fcn solver - backtrack
def solve( M ):
    solution = [];
    # TODO
    return solution

## fcn solver
# TODO


   
## DEBUG
def DB_print( M ):
    # TODO compactize
    for y in range( len(M) ):
        for x in range( len(M[0]) ):
            print "\t%.2f"%M[y][x],
        print ""



## START                                                                        
if __name__ == '__main__':

    ## [ y x ]
    GOAL=[40, 60]
    START=[0, 0]

    ## init 2D matrix
    # TODO compactize    
    M = []
    row = []
    col = []
    for y in range(YMAX):
        row=[]
        for x in range(XMAX):
            row+=[0]
        col += [row]
    M = col


    # TODO distance
    for y in range(YMAX):
        for x in range(XMAX):
            M[y][x] = distance( [y, x], GOAL )

    # TODO normalize
    M = normalize( M )


    DB_print( M )  

    sys.exit(0)                   


    ## repulsive potential field
#    M = repulsive_potential_field( M )
#    M = normalize( M )
    # TODO display

    ## attractive potential field
#    M = attractive_potential_field( M )
#    M = normalize( M )
    # TODO display

    ## path solving
    # TODO

    ## visualization
    # TODO

    print "READY.",


    
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # X = np.arange(-5, 5, 0.25)
    # Y = np.arange(-5, 5, 0.25)

#    Y = range(len(M))
    Y = np.arange(0,YMAX,1)
#    X = range(len(M[0]))
    X = np.arange(0,XMAX,1)
    X, Y = np.meshgrid(X, Y)

# TODO rm    
    # R = np.sqrt(X**2 + Y**2)
    # Z = np.sin(R)
    

    Z = M

    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
