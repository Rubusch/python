#!/usr/bin/python3

def fun1(a, b, c, d, e, f, g):
    print('fun1:', a, b, c, d, e, f, g)

def fun2(*args):
    print('fun2:', args)

    ## convert tuple into a list so that we can modify it
    args = list(args)

    args[0] = 'I'
    args[1] = 'have'

    fun1(*args)

fun2("There's", "no", "fun", "with", "Claudia", "and", "Anja.")

print('READY.')
