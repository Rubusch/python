#!/usr/bin/python3

## ask user, read in user input

## NB: in python2 use 'raw_input()' instead of 'input()'
## NB: w/o 'int()' python implicitely generates a 'str' type and no 'int' type!
x = int(input("enter an integer: "))

if x < 0:
    x = 0
    print('negative changed to zero')

elif x == 0:
    print('zero')

elif x == 1:
    print('single')

else:
    print('value is: ', x)


print("READY")
