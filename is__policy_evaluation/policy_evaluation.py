#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment04 for Intelligent Systems
#
# author: Lothar Rubusch
# email: l.rubusch@gmx.ch
#
#
# Given:
#
#     x0123456x
#    y#########
#    0#.......#
#    1#.S#....#
#    2#.##....#
#    3#..#..#.#
#    4#.....#G#
#    y#########
#
# Figure 1: 30-State Maze. For all questions refer to this figure. The agent has
# four possible actions: North, South, East, West. When the agent takes an
# action, it goes to the adjacent state in the chosen direction with probability
# 0.70, and in one of the other directions with probability 0.30. For example,
# if the agent chooses North, then there is a 70% chance that it actually goes
# North, a 10% chance it will go South, 10% it will go West, and 10% it will go
# East. If the agent goes in a direction that will take it outside the maze
# (e.g. going South in S), it stays in the same state. The reward r is 0 for all
# state transitions, except that when entering the goal state G the reward is
# 10.0. The discount factor gamma is set to 0.9. The agent cannot leave the goal
# state. You may number the states any way you want.
#
#
# Question 1.
#
# A. (35 points) Implement Policy Evaluation. Starting with V (s) = 0, for all
# of s, and assuming a random policy (pi(s, a) = 1/4, for all of s, a), what are
# the final values, V (s), after the evaluation has converged?
#
# B. (10 points) How and why do the values change if the discount factor, gamma
# is changed to 0.7 (again starting with V (s) = 0, for all of s)?
#
#
# Policy Evaluation Algorithm
#
#     Input pi, the policy to be evaluated
#     Initialize V(s) = 0, for all s element of S+
#     Repeat
#         delta <- 0
#         For each s element of S:
#             ny <- V(s)
#             V(s) <- sum_a{ pi(s, a) sum_s, P_ss'^a, [R_ss'^a + gamma*V(s')]
#             delta <- max( delta, |ny - V(s)|)
#     until delta < theta // (theta - a small positive number)
#     Output V ~ V^pi
##

## sys.exit()
import sys

## plotting library
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from matplotlib import cm # color settings

def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )

class Pos( object ):
    _x = 0.0
    _y = 0.0
    _reward=0.0
    _wall=False
    _value=0.0
    _delta=0.0
    def __init__( self, x, y, reward=0.0, wall=False, value=0.0, delta=0.0):
        self._x = x
        self._y = y
        self._reward=reward
        self._wall=wall
        self._value=value
        self._delta=delta

    def x(self):
        return self._x

    def y(self):
        return self._y

    def setx(self, x):
        self._x = x

    def sety(self, y):
        self._y = y

    def reward(self):
        return self._reward

    def setreward(self, reward):
        self._reward=reward
        self._value=reward

    def iswall(self):
        return self._wall

    def setwall(self):
        self._wall=True
#        self._value="."   
        self._value=0.0   

    def value(self):
        return self._value

    def setvalue(self,value):
        self._value=value

    def delta(self):
        return self._delta

    def setdelta(self,delta):
        self._delta=delta

    def __str__(self):
#        return str(self._delta)
        return str(self._value)




class Agent(object):
    _maze=[]
    def __init__(self, maze):
        self._maze=maze

    def print_maze(self):
        for y in range(len(self._maze)):
            for x in range(len(self._maze[y])):
                print maze[y][x],"\t",
            print ""

    def isout(self, y, x):
        if maze[y][x].iswall(): return True
        return False

    def direction(self,pos,dy,dx,pdir):
# FIXME no difference by different gammas ?!
        gamma = 0.9
#        gamma = 0.7
        ## check if s' is out
        if self.isout( pos.y()+dy, pos.x()+dx): return
        ny = pos.value()
        reward = pos.reward() # TODO which reward?
        delta = pos.delta()
        nextValue = maze[pos.y()+dy][pos.x()+dx].value()
# TODO check summation
        
        value = ny
        value += 0.75 * pdir * (reward + gamma * nextValue)
        
#        value = 0.75 * pdir * (reward + gamma * nextValue)
        
        delta = max(delta, abs(ny-value)) # max( delta, | ny - value | )
        ## write back
        pos.setvalue(value) # TODO check if maze is updated by this   
        pos.setdelta(delta)

    def updatestate(self,pos,dy,dx):
        if 0 == dy and 1 == dx: self.direction(pos,dy,dx,0.7)
        else: self.direction(pos,dy,dx,0.1)

        if 1 == dy and 0 == dx: self.direction(pos,dy,dx,0.7)
        else: self.direction(pos,dy,dx,0.1)

        if 0 == dy and -1 == dx: self.direction(pos,dy,dx,0.7)
        else: self.direction(pos,dy,dx,0.1)

        if -1 == dy and 0 == dx: self.direction(pos,dy,dx,0.7)
        else: self.direction(pos,dy,dx,0.1)

    def normalize(self):
        maxval = 0  
#        maxdelta = 0
        for y in range(len(self._maze)):
            for x in range(len(self._maze[0])):
                if self.isout(y,x): continue
                maxval = max( maxval, maze[y][x].value() )  
#                maxdelta = max( maxdelta, maze[y][x].delta() )

        for y in range(len(self._maze)):
            for x in range(len(self._maze[0])):
                if self.isout(y,x): continue
                if 0 != maxval: maze[y][x].setvalue(maze[y][x].value() / maxval)  
                else: maze[y][x].setvalue(0)  
#                if 0 != maxdelta: maze[y][x].setdelta(maze[y][x].delta() / maxdelta)
#                else: maze[y][x].setdelta(0)



    def plot(self):
        xs = []
        for i in range(len(self._maze)):
            xs += range(len(self._maze[0]))

        ys = []
        for i in range(len(self._maze[0])):
            ys += range(len(self._maze))

        zs = []
        for y in range(len(self._maze)):
            for x in range(len(self._maze[y])):
                zs.append( maze[y][x].value() ) ## value
#                zs.append( maze[y][x].delta() ) ## value

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
#        ax = fig.gca(projection='3d')

        ax.scatter(xs,ys,zs)
#        ax.plot_surface(xs,ys,zs, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#        ax.plot_surface(xs,ys,zs)

#        X,Y = np.meshgrid(xs,ys)
#        ax.plot_surface(X,Y,zs)

#        ax.plot_wireframe(xs,ys,zs)
#        ax.plot_trisurf(xs,ys,zs)

#        ax.set_xlabel('X Label')
#        ax.set_ylabel('Y Label')
#        ax.set_zlabel('Z Label')

        plt.show()
#        Axes3D.scatter(xs, ys, zs)



    def policy(self):

        for i in range(20): # TODO repeat until delta < theta   
            ## foreach position s element of S
            for y in range(len(self._maze)):
                for x in range(len(self._maze[y])):

                    ## check if s is out
                    if self.isout(y,x): continue

                    ## permutate all directions
                    self.updatestate(maze[y][x], 0, 1)
                    self.updatestate(maze[y][x], 0,-1)
                    self.updatestate(maze[y][x], 1, 0)
                    self.updatestate(maze[y][x],-1, 0)

#        self.normalize()
        self.plot()
# TODO 
# p(dir) = 0.7
# p(rest) = 0.1; sum = 0.3
# V(s) = 0
# pi(s, a) = 0.25
if __name__ == '__main__':

    ymax = 5 + 2
    xmax = 7 + 2

    ## initialize V(s)=0 for all elements of S(maze)
    maze=[]
    for y in range(ymax):
        line=[]
        for x in range(xmax):
            pos = Pos(x,y)

            ## set boundaries
            if y == 0 or y == ymax-1: pos.setwall()
            if x == 0 or x == xmax-1: pos.setwall()

            ## set inside borders
            if x==3 and y==2: pos.setwall()
            if x==2 and y==3: pos.setwall()
            if x==3 and y==3: pos.setwall()
            if x==3 and y==4: pos.setwall()
            if x==6 and y==4: pos.setwall()
            if x==6 and y==5: pos.setwall()

            ## goal
            if x==7 and y==5: pos.setreward(10)

            line += [pos]
        maze.append(line)

    ## start algorithm
    agent=Agent(maze)
    agent.policy()

           
    agent.print_maze()

    print "READY."
