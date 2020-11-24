#!/usr/bin/python3

arr = [ 'a', 'b', 'c' ]
print('string, raw:\t', arr)

out = '.'.join(arr)
print('dot separated:\t',out)

arr = [ 1, 2, 3 ]
print('int, raw:\t', arr)

out = '.'.join(["%s" % el for el in arr])
print('dot separated:\t',out)

print("READY.")
