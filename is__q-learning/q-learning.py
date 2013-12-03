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
# Question 2.
#
# A. (40 points) Implement Q-learning with learning rate alpha = 0.4. Initialize Q(s, a) = 0, for all s, a.
# Starting each episode in state S, run Q-learning until it converges, using an -greedy policy.
# Each episode ends after 100 actions or once the goal, G, has been reached, whichever happens
# first.
#
# B. (10 points) Plot the accumulated reward for the run, i.e. plot the total amount of reward received
# so far against the number of episodes, and show the greedy policy with respect to the value
# function.
#
# Question 3.
#
# (15 points) If instead of moving N,S,E,W, the agent moves like a knight in chess (for
# example, one step North, then two steps East, in one move), how would the value of the states
# change (run Q-learning with this new action set)? So the agent now has 8 possible moves. If an
# action would take it outside the maze, it stays where it is. The probability for moving according
# to the chosen action is 72% and 4% for each of the other 7 actions.
#
#
# Q-learning
#
# Initialize Q(s,a) arbitrarily
# Repeat (for each episode):
#     Initialize s
#     Repeat (for each step of episode):
#         Choose a from s using policy derived from Q (e.g. epsilon-greedy)
#         Take action a, observe r, s'
#         Q(s,a) <- Q(s,a) + alpha * [r + gamma * max_a'(Q(s',a') - Q(s,a))]
#         s <- s'
#     until s is terminal
##

## sys.exit()
import sys

## DEBUG plotting library
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

## random number generator, randrange() or random()
import random


def die( msg = "" ):
    print "FATAL",
    if 0 < len(str(msg)):
        print ": " + str(msg)
    sys.exit( -1 )

class Position( object ):
    _x = 0.0
    _y = 0.0
    _reward=0.0
    _wall=False
    _value=0.0
    def __init__( self, y, x, reward=0.0, wall=False, value=0.0):
        self._x = x
        self._y = y
        self._reward=reward
        self._wall=wall
        self._value=value

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
        self._value=0.0

    def value(self):
        return self._value

    def setvalue(self,value):
        self._value=value

    def __str__(self):
        return str(self._value)



class Agent(object):
    _maze=[]
    _gamma=1.0
    def __init__(self,maze,gamma,alfa,ystart,xstart,ygoal,xgoal):
        self._maze=maze
        self._gamma=gamma
        self._alfa=alfa
        self._xstart=xstart
        self._ystart=ystart
        self._xgoal=xgoal
        self._ygoal=ygoal
        self.NORTH=0
        self.EAST=1
        self.SOUTH=2
        self.WEST=3

    def print_maze(self):
        for y in range(len(self._maze)):
            for x in range(len(self._maze[y])):
#                print "%.7f\t"% maze[y][x].value(), # rounded values
                print maze[y][x],"\t", # raw values
            print ""

    def isout(self, y, x):
        if maze[y][x].iswall(): return True
        return False

    def direction(self, pos):
        # NORTH=0
        # EAST=1
        # SOUTH=2
        # WEST=3
        direction = random.randrange(0,4)
        if direction == self.NORTH: pos=self.move(pos,1,0)
        elif direction == self.EAST: pos=self.move(pos,0,1)
        elif direction == self.SOUTH: pos=self.move(pos,-1,0)
        elif direction == self.WEST: pos=self.move(pos,0,-1)
        return pos


    # def direction(self,pos,dy,dx,pdir,delta,value):
    #     gamma = self._gamma

    #     ## check if s' is out
    #     if self.isout( pos.y()+dy, pos.x()+dx): return delta,value
    #     ny = pos.value()
    #     reward = pos.reward()
    #     nextValue = maze[pos.y()+dy][pos.x()+dx].value()
    #     value += 0.25 * pdir * (reward + gamma * nextValue)
    #     return delta,value


    # def updatestate(self,pos,dy,dx,delta,value):
    #     ## 2. permutation by probability towards a specified direction
    #     if 0 == dy and 1 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
    #     else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)

    #     if 1 == dy and 0 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
    #     else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)

    #     if 0 == dy and -1 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
    #     else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)

    #     if -1 == dy and 0 == dx: delta,value=self.direction(pos,dy,dx,0.7,delta,value)
    #     else: delta,value=self.direction(pos,dy,dx,0.1,delta,value)
    #     return delta,value

    def max_next(self,pos):
        val=0
        if not self.isout(pos.y()+1,pos.x()): val=max(val,maze[pos.y()+1][pos.x()].value())
        if not self.isout(pos.y()-1,pos.x()): val=max(val,maze[pos.y()-1][pos.x()].value())
        if not self.isout(pos.y(),pos.x()+1): val=max(val,maze[pos.y()][pos.x()+1].value())
        if not self.isout(pos.y(),pos.x()-1): val=max(val,maze[pos.y()][pos.x()-1].value())

        if 0 < val: print "IN ",val   

        return val

    def move(self,pos,dy,dx):
        if self.isout(pos.y()+dy, pos.x()+dx): return pos

        ## Q update
        q_old = pos.value()
        q_next = self._maze[pos.y()+dy][pos.x()+dx].value()
        alfa = self._alfa
        reward = pos.reward()
        gamma = self._gamma

        q_value = q_old + alfa * (reward + gamma * self.max_next(pos) - q_old)
        print "OUT ",q_value  

        pos.setvalue(q_value)

        ## move
        pos.sety(pos.y()+dy)
        pos.setx(pos.x()+dx)

        return pos


    def q_learning(self):
        cnt=0
        
        pos = Position(self._ystart, self._xstart)
        print "start: x=%d, y=%d"%(pos.x(),pos.y())
        while True:
            pos=self.direction(pos)
            print "move: x=%d, y=%d"%(pos.x(),pos.y())

            if self._ygoal==pos.y() and self._xgoal==pos.x():
                print "GOAL"
                break





            ## break out
#            if 10 == cnt: break
#            cnt += 1







            
# TODO rm
        #     ## init delta per round
        #     delta = 0

        #     ## foreach position s element of S
        #     for y in range(len(self._maze)):
        #         for x in range(len(self._maze[y])):

        #             ## load value for next round
        #             value = 0

        #             ## check if s is out
        #             if self.isout(y,x): continue

        #             ## 1. permutation by possible directions
        #             delta,value=self.updatestate(maze[y][x], 0, 1, delta,value)
        #             delta,value=self.updatestate(maze[y][x], 0,-1, delta,value)
        #             delta,value=self.updatestate(maze[y][x], 1, 0, delta,value)
        #             delta,value=self.updatestate(maze[y][x],-1, 0, delta,value)

        #             ## compare differences after 4 x 4 permuted additions
        #             ny = maze[y][x].value()
        #             delta = max(delta, abs(ny-value)) # max( delta, | ny - value | )

        #             ## store resulting value
        #             maze[y][x].setvalue(value)

        #     ## check delta
        #     print "%d. iteration, delta: %.7f > %.7f" % (cnt,delta,self._convergence)
        #     if delta < self._convergence:
        #         print "STOP"
        #         break

        #     ## increment loop iteration
        #     cnt+=1

        # ## // while


## DEBUG printouts
    ## boundary - cuts off very high values
    def DEBUG_plot(self,boundary=1.0):
        xs = []; xb = []
        ys = []; yb = []
        zs = []; zb = []
        for y in range(len(self._maze)):
            for x in range(len(self._maze[y])):
                if self.isout(y,x):
                    xb.append(x)
                    yb.append(-y)
                    zb.append(0.0)
                else:
                    val = str(maze[y][x])
                    if float(val) >= boundary:
                        zs.append( boundary )
                    else:
                        zs.append( float(val) ) ## take default  by Position str()
                    xs.append(x)
                    ys.append(-y)
                
## plot_surface
#        y = np.arange(-len(self._maze), 0.0, 1.0)
#        x = np.arange(0.0, len(self._maze[0]), 1.0)
#        X, Y = np.meshgrid(x,y)
#        zs = np.array([z for z in zs])
#        Z = zs.reshape(X.shape) 
#        fig = plt.figure()
#        ax = fig.add_subplot(111, projection='3d')
#        ax.plot_surface(X, Y, Z)
#        plt.show()

        
## delaunay
#        from mayavi import mlab
#        X = np.array(xs)
#        Y = np.array(ys)
#        Z = np.array(zs)
#        pts = mlab.points3d(X,Y,Z,Z)
#        mesh = mlab.pipeline.delaunay2d(pts)
#        pts.remove()
#        surf = mlab.pipeline.surface(mesh)
#        mlab.show()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xs,ys,zs,s=50,c="#FFD700") # values, yellow
#        ax.scatter(xs,ys,zs,s=50,c="#FF3300") # values, red
#        ax.scatter(xs,ys,zs,s=50,c="#FF3300") # values, blue

        ax.scatter(xb,yb,zb,s=100,c="#838B8B") # boundary

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()
## // DEBUG printouts
        



if __name__ == '__main__':

    ymax = 5 + 2
    xmax = 7 + 2
    LIMIT = 7 #digits

    ## initialize V(s)=0 for all elements of S(maze)
    ystart=2
    xstart=2
    ygoal=5
    xgoal=7
    maze=[]
    for y in range(ymax):
        line=[]
        for x in range(xmax):
            pos = Position(y,x)

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
            if x==xgoal and y==ygoal: pos.setreward(10)

            line += [pos]
        maze.append(line)

    ## start algorithm

    ## Exercise 2a)
    print "Exercise 2a)"
    gamma=0.9
    alfa=0.4
    agent=Agent(maze,gamma,alfa,ystart,xstart,ygoal,xgoal)
    agent.q_learning();
    agent.print_maze()

    agent.DEBUG_plot()

    print "READY."
