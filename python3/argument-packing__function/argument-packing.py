#!/usr/bin/python3

def fun(a, b, c, d):
    print(a, b, c, d)

values = [1, 2, 3, 4]

## use argument unpacking to match function arguments by list elements directly
fun(*values)

print('READY.')
