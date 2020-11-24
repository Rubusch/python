#!/usr/bin/python3

val = "asdf-1.2.3"
print("val '%s'" % val)

## replace '.' by '_'

## syntax python2
#import string
#print("val '%s'" % string.replace( val, '.', '_'))

## syntax: python3
print("val '%s'" % val.replace('.', '_'))


print("READY.\n")
