## Fibonacci numbers module
##
## REFERENCE: https://docs.python.org/3/tutorial/modules.html
##
## usage:
## $ python3
## >>> import fobo
## >>> fobo.fib(1000)
##    <output>
##
## To speed up loading modules, Python caches the compiled version of each
## module in the __pycache__ directory under the name module.version.pyc,
## where the version encodes the format of the compiled file; it generally
## contains the Python version number. For example, in CPython release 3.3
## the compiled version of spam.py would be cached as
## __pycache__/spam.cpython-33.pyc. This naming convention allows compiled
## modules from different releases and different versions of Python to
## coexist.

def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while b < n:
        print(b,)
        a, b = b, a+b

def fib2(n): # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result

