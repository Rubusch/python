#!/usr/bin/python3
## lambda computes the volume of a cube

## usage map(function, sequence)
##
## calls function(item) for each of the sequence's items and returns a list of
## the return values
print(*map( lambda x: x*x*x, range(1, 11) ))

print("READY.")

