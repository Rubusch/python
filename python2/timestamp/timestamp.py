#!/usr/bin/env python

import datetime
print datetime.datetime.utcnow() 

print datetime.datetime.now()

# extract something for filenames
ext = str( datetime.datetime.now() ).replace(' ', '-').replace(':','-').split('.')[0]

print ext

print "READY.\n"

