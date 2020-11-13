#!/usr/bin/python3
##
## NB: don't call this file 'subprocess.py' then subprocess.run() will stop working!!!

#import os.system
import subprocess

## before python3.5
#subprocess.call(["ls", "-l"])

## after python3.5
subprocess.run(["ls", "-la"])

print("READY.")
