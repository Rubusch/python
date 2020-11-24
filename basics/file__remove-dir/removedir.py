#!/usr/bin/python3

import os
import re

## remove files and folders by provided name pattern
def rmpattern( path, pattern ):
    pattern = re.compile( pattern )
    for each in os.listdir(path):
        if pattern.search(each):
            name = os.path.join(path,each)
            try: os.remove(name)
            except:
                rmpattern(name, '')
                os.rmdir(name)


text = """jack and jill went up the hill to fetch a pail of water
jack fell down and broke his crown 
and jill came tumbling after
"""

foldername = './folder'

if os.path.exists(foldername):
    print("delete folder and content")
    regex = re.compile('folder')
    rmpattern( './', regex)

else:
    print("create file and folder with content")
    os.mkdir(foldername)
    FILE = open(foldername + '/test.txt', 'w')
    FILE.write(text)
    FILE.close()


## alternatively in python3 use shutil
import shutil

print('..and remove the folder again using shutil')
shutil.rmtree(foldername, ignore_errors=True)

print("READY.")

