#!/usr/bin/python3
##
## changes from python2 to python3

import sys
print('python version: ', sys.version)

my_generator = (letter for letter in 'abcdefg')

print('next():', next(my_generator))

## python2 allows this
#print('.next():')
#my_generator.next()

## Since next() (.next()) is such a commonly used function (method),
## this is another syntax change (or rather change in implementation)
## that is worth mentioning: where you can use both the function and
## method syntax in Python 2.7.5, the next() function is all that
## remains in Python 3 (calling the .next() method raises an
## AttributeError).

print('READY.')
