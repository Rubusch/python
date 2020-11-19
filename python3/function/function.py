#!/usr/bin/python3

def fib(n):
    """print a fibonacci series up to n"""
    result = []
    a, b = 0, 1
    while b < n:
        print(b,)
        result.append(b)
        a, b = b, a+b
    return result

# call
f2000 = fib(2000)
print(f2000, "\nREADY.")
