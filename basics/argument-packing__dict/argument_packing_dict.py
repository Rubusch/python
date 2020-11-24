#!/usr/bin/python3
##
## ** is for dictionaries

def fun(a, b, c):
    print(a, b, c)

## a call with unpacking a dict
d = {'a':6654, 'b':7794, 'c':9400}


## UNPACKING
print('we expect to see just the key values!')
fun(**d)
## Here ** unpacked the dictionary used with it, and passed the items in the
## dictionary as keyword arguments to the function. So writing 'fun(1, **d)' was
## equivalent to writing 'fun(1, b=4, c=10)'


## PACKING
def fum(**kwargs):
    print('type:',type(kwargs))

    print('\ncontent:')
    for key in kwargs:
        print('%s : %s' % (key, kwargs[key]))

    print('')

fum(claudia=48, katja=38, anja=28)

print('READY.')
