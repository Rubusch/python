#!/usr/bin/python3
##
## changes from python2 to python3
##
## REFERENCE: https://docs.python.org/3/library/timeit.html

import timeit

def test():
    """Stupid test function"""
    L = [i for i in range(100)]

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("test()", setup="from __main__ import test"))
    print('READY.')
