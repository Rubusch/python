#!/usr/bin/python3
##
## NB: don't call this file 'subprocess.py' then subprocess.run() will stop working!!!

#import os.system
import subprocess

try:
    ## before python3.5
    #subprocess.call(["ls", "-l"])

    ## after python3.5
    res = subprocess.run(["ls", "-la"])
	res.check_returncode() # in case raises exception
	print('if we reach this, no exception was thrown...')
except subprocess.CalledProcessError as e:
    print(e.output)

print("READY.")
