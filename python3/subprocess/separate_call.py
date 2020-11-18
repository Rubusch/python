#!/usr/bin/python3
##
## NB: don't call this file 'subprocess.py' then subprocess.run() will stop working!!!

#import os.system
import subprocess

try:
    ## before python3.5
    #subprocess.call(["ls", "-l"])

    ## after python3.5
    subprocess.run(["ls", "-la"])
except subprocess.CalledProcessError as e:
    print(e.output)

print("READY.")
