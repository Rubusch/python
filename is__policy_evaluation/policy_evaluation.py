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

class Pos( object ):
    _x = 0
    _y = 0
    def __init__( self, x, y):
        self._x = x
        self._y = y
        
    def x(self):
        return self._x

    def y(self):
        return self._y

    def setx(self, x):
        self._x = x

    def sety(self, y):
        self._y = y

    def __str__(self):
        return "[" + str(self._x) + ":" + str(self._y) + "]"



class Agent(object):
    _x_limit=""
    _y_limit=""
    _maze=[]
    def __init__(self, maze):
        self._maze=maze
        self._y_limit=len(self._maze)
        self._x_limit=len(self._maze[0])
#        print "XXX x-limit: " + str(self._x_limit) + ", y-limit: " + str(self._y_limit)


    def move_north(self, pos):
        y=pos.y()
        y=y-1
        if(0>y):
            print "BORDER - NORTH"
        else:
            pos.sety(y)
        return pos

    def move_south(self, pos):
        y=pos.y()
        y=y+1
        if(self._y_limit<=y):
            print "BORDER - SOUTH"
        else:
            pos.sety(y)
        return pos

    def move_west(self, pos):
        x=pos.x()
        x=x-1
        if(0>x):
            print "BORDER - WEST"
        else:
            pos.setx(x)
        return pos

    def move_east(self, pos):
        x=pos.x()
        x=x+1
        if(self._x_limit<=x):
            print "BORDER - EAST"
        else:
            pos.setx(x)
        return pos

    def print_maze( self ):
        for y in len(self._maze):
            for x in len(self._maze[y]):
                print maze[y][x],
            print ""



# TODO 
# p(dir) = 0.7
# p(rest) = 0.1; sum = 0.3
# V(s) = 0
# pi(s, a) = 0.25
if __name__ == '__main__':

    maze=[[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 0, 0],
          [0, 1, 1, 0, 0, 0, 0],
          [0, 0, 1, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 1, 2]]

    agent=Agent(maze)

    agent.print_maze()

    print "READY."
