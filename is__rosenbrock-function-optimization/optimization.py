#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment05 for Intelligent Systems
#
#
# Question 2.
#
# Implement (1+lambda)-ES to optimize the following function:
# sum{i=1;N-1} [(1 - xi )2 + 100(xi+1 - x2 )2 ]
#
# known as the Rosenbrock function (http://en.wikipedia.org/wiki/Rosenbrock_function),
# where N is the number of dimensions, and -5 <= xi <= 10, i = 1, 2, . . . , N .
# A. (40 points) Run the algorithm 10 times for each of the following four settings, N = 5, 10, 20, 50.
# Choose your own lambda.
# B. (10 points) Plot the average fitness (over the 10 runs) of the parent in each generation for each
# N . As with question 1B, there should be four curves here.
#
#
# author: Lothar Rubusch
# email: l.rubusch@gmx.ch


import sys # sys.exit()

import matplotlib.pyplot as plt # plotting

def die(msg=""):
    print "FATAL",
    if 0 < len(str(msg)):
        print ":"+str(msg)
    sys.exit(-1)


class Problem(object):
    def __init__(self, problem=0, strategy=1, fitness=0):
        self._problem=problem
        self._strategy=strategy
        self._fitness=fitness
    def problem(self): return self._problem
    def strategy(self): return self._strategy
    def fitness(self): return self._fitness
# TODO setter?

class Evolution(object):
    def __init__(self, ndims, noffspring):
        self.ndims=ndims
        self.noffspring=noffspring
        # TODO 
        pass 

    def run(self):
## 1. initialize parents and evaluate them
## 2. create some offspring by perturbing parents with Gaussian noise according to parent's mutation parameters
## 3. evaluate offspring
## 4. select new parents from offspring and possibly old parents
## 5. if good solution not found go to 2
        # TODO  
        pass 

    def compute_fitness(self, problem_params):
        fitness=0.0
        for idx in range(self.ndims-1):
            x = problem_params[idx]
            x_next = problem_params[idx+1]
#            fitness += ((1 - x)** + 100 * (x_next + x**)** )
            fitness += ((1-x)*(1-x)+100*(x_next+x*x)*(x_next+x*x))

    def __str__(self):
        return str("TODO")   


                                                                               
## MAIN
if __name__ == '__main__':
    ndims = 5
    noffspring = 20

    evolution = Evolution(ndims, noffspring)
    print evolution  

    # TODO  
    print "READY."
