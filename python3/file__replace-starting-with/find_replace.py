#!/usr/bin/python3
##
## find line starting with 'pattern' and replace bby 'newtext' using fileinput
## should also cut off leading spaces (before 'pattern')

import sys
import fileinput

from shutil import copy

pattern = 'jack '
newtext = 'all work and no play makes jack a dull boy...'


## version using 'startswith()'
filename = 'test__startswith.txt'
copy('test.txt.template', filename)

for line in fileinput.input([filename], inplace=True):
    if line.strip().startswith(pattern):
        line = newtext + '\n'
    sys.stdout.write(line)
fileinput.close()


## version using regexp
filename = 'test__regexp.txt'
copy('test.txt.template', filename)

for line in fileinput.input([filename], inplace=True):
    line = re.sub(r"^\s*"+pattern, newtext, line)
    sys.stdout.write(line)
fileinput.close()

print('READY.')
