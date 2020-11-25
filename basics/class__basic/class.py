#!/usr/bin/python3

class Complex:
    ## __init__ is a special function for initialization of an object to a specific values
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

if __name__ == '__main__':

    x = Complex(1.2, -3.4)

    print(x.r, x.i)
    print('READY.')


