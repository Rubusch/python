#!/usr/bin/python3

## apply function inside a filter, provide a list as argument
def f(x): return x % 2 != 0 and x % 3 !=0

# usage of filter( function, sequence ):
# returns a sequence consisting of those items from the sequence for which
# function(item) is true; the result will be of the same type, otherwise
# defaults to list

## in python2
#print(filter( f, range(2, 25) ))

## in python3
## - use 'argument unpacking' for range(), and put in a list: [*range()]
## - same for filter
print( [*filter(f, [*range(2, 25)] )] )


## alternative use a lambda
print( [*filter(lambda x: x % 2 != 0 and x % 3 !=0, [*range(2, 25)] )] )

print("READY.")
