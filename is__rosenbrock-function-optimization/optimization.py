#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# Assignment05 for Intelligent Systems
#
# Question 2. Implement (1+lambda)-ES to optimize the following function:
# N -1
# [(1 - xi )2 + 100(xi+1 - x2 )2 ]
# i
# f (x) =
# i=1
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


## 1. initialize parents and evaluate them
## 2. create some offspring by perturbing parents with Gaussian noise according to parent's mutation parameters
## 3. evaluate offspring
## 4. select new parents from offspring and possibly old parents
## 5. if good solution not found go to 2


class Evolution(object):
    def __init__(self):
        # TODO 
        pass



                                                                               
## MAIN
if __name__ == '__main__':


# TODO  
print "READY."
