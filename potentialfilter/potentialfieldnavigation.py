#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

#import math
from math import *
import sys

## 3D plotting
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

## globals
# TODO         
## size of robot = 7
#XSIZE=300 / 7
XSIZE=43
#YSIZE=200 / 7
YSIZE=29
XMAX=XSIZE-1
YMAX=YSIZE-1

## [ y x ]
GOAL=[YMAX, XMAX]
START=[0, 0]

## distance
def distance( pktsrc, pktdst ):
    dist = 0
    dists=[]
    try:
        for elem in pktdst:
            dy = pktsrc[0] - elem[0]
            dx = pktsrc[1] - elem[1]
            dists += [sqrt(dx**2 + dy**2)]
        dist = min(dists[:])
    except TypeError:
        dy = int(pktsrc[0]) - int(pktdst[0])
        dx = int(pktsrc[1]) - int(pktdst[1])
        dist = sqrt(dx**2 + dy**2)
    return dist

## normalize
def normalize( M ):
    maxvals = []
    maxval = -1
    for y in range( len(M) ):
        maxvals += [max([elem for elem in M[y]])]
    maxval = max( maxvals[:] )
    try:
        for y in range( len(M) ):
            for x in range( len(M[0]) ):
                M[y][x] = M[y][x] / maxval
    except ZeroDivisionError:
        print "ERROR: maxval was zero: ", maxval
        sys.exit( -1 )

## visualization of results
def visualize( Z ):
    Y = np.arange(0,YMAX,1)
    X = np.arange(0,XMAX,1)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(X, Y)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    ax.set_zlim(0.0, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

## obstacle
def obstacle( M, obs ):
    k_rep = 5
    rho_zero = 20
    U_rep = 0
    U_obs = 0
    for y in range(YMAX):
        for x in range(XMAX):
            dobs = distance( [y, x], obs )
            if 0 == dobs:
                U_rep = float(k_rep)
            else:
                U_rep = float(M[y][x]) + 0.5 * float(k_rep) * (1.0 / float(dobs) - 1.0 / float(rho_zero) )**2
                if k_rep < U_rep: U_rep = k_rep
            M[y][x] = U_rep

## repulsive_potential_field
def repulsive_potential_field( M ):
    obstcs = [[10,10],[10,20],[10,30],[10,40],  [20,10],[20,20],[20,30],[20,40], [15,35]]

    for obs in obstcs:
        obsy = obs[0]
        obsx = obs[1]
        obstacle( M, [ [obsy,obsx-1], [obsy-1,obsx], [obsy,obsx], [obsy+1,obsx], [obsy,obsx+1] ] )


## attractive_potential_field
def attractive_potential_field( M ):
    ## distance matrix for attraction potential
    k_att = 2
    dist = 0
    for y in range(YMAX):
        for x in range(XMAX):
            dist = distance( [y, x], GOAL )
            M[y][x] = 0.5 * float(k_att) * float(dist)**2
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
    ## init 2D matrix
    M = []
    M += [[0 for x in range(XMAX)] for y in range(YMAX)]


    ## attractive potential field
#    M = attractive_potential_field( M )
#    M = normalize( M )
#    visualize( M )



    ## repulsing potential field
#    M = repulsive_potential_field( M )
    repulsive_potential_field( M )
#    M = normalize( M )
    normalize( M )

    ## visualize
    visualize( M )

    sys.exit(0)                   
#    DB_print( M )  



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
    sys.exit(0)                   


    


