#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01


## fcn distance
def distance( pktsrc, pktdst ):
    dists=[]
    for i in size(dst[]):
        dx= pktsrc[1] - pktsrc[i, 1]
        dx= pktsrc[2] - pktsrc[i, 2]
    # TODO
    return dist

## fcn normalize
def normalize( M ):
    # TODO
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

    
## START                                                                        
if __name__ == '__main__':
    XMAX=60
    YMAX=40
    M[YMAX][XMAX]
    GOAL=(40, 60)
    START=(0, 0)

    ## repulsive potential field
    M = repulsive_potential_field( M )
    M = normalize( M )
    # TODO display

    ## attractive potential field
    M = attractive_potential_field( M )
    M = normalize( M )
    # TODO display

    ## path solving
    # TODO

    ## visualization
    # TODO


    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.ticker import LinearLocator, FormatStrFormatter
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X = np.arange(-5, 5, 0.25)
    Y = np.arange(-5, 5, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    ax.set_zlim(-1.01, 1.01)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
