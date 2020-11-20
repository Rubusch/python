#!/usr/bin/python3
##
## find line starting with 'pattern' and replace bby 'newtext' using fileinput
## should also cut off leading spaces (before 'pattern')

import sys
import fileinput

filename = 'test.txt'
pattern = 'jack '
newtext = 'all work and no play makes jack a dull boy...'

import shutil
shutil.copy('test.txt.template', filename)

for line in fileinput.input([filename], inplace=True):
    if line.strip().startswith(pattern):
        line = newtext + '\n'
    sys.stdout.write(line)

print('READY.')
