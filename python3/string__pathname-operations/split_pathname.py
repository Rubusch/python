#!/usr/bin/python3

import os

mesg = '/a/b/c/'

print('message:', mesg)
## strips exactly a trailing slash, or does nothing if there is none
print('cut off trailing slash, if exists:\t', mesg.strip('/'))
foo = mesg.strip('/')
print('cut off trailing slash, if exists:\t', foo.strip('/'))
print('')

print('message:', mesg)
## ignores trailing slash, if existing
print('cut off ANY trailing element (in case together with trailing /):\t', mesg.rsplit('/', 1)[0])
foo = mesg.rsplit('/', 1)[0]
print('cut off ANY trailing element (in case together with trailing /):\t', foo.rsplit('/', 1)[0])
print('')

print('message:', mesg)
## needs a strip() before, or trailing slash will be evaluated
print('cut off the last dirname:\t\t', os.path.dirname( mesg.strip('/') ))
print('cut off the last basename:\t\t\t', os.path.basename( mesg.strip('/') ))
print('')

print("READY.")
