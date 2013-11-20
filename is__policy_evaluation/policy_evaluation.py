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
#     #########
#     #.......#
#     #.S#....#
#     #.##....#
#     #..#..#.#
#     #.....#G#
#     #########
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

# TODO 
