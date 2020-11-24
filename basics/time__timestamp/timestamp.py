#!/usr/bin/python3

import datetime
print(datetime.datetime.utcnow())
print(datetime.datetime.now())

# extract something for filenames
ext = str( datetime.datetime.now() ).replace(' ', '-').replace(':','-').split('.')[0]
print(ext)

stamp = str( datetime.datetime.now() ).replace('-','').split(' ')[0]
print(stamp)

print("READY.\n")

