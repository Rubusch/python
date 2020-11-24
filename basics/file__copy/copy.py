#!/usr/bin/python3
##
## ┌──────────────────┬────────┬───────────┬───────┬────────────────┐
## │     Function     │ Copies │   Copies  │Can use│   Destination  │
## │                  │metadata│permissions│buffer │may be directory│
## ├──────────────────┼────────┼───────────┼───────┼────────────────┤
## │shutil.copy       │   No   │    Yes    │   No  │      Yes       │
## │shutil.copyfile   │   No   │     No    │   No  │       No       │
## │shutil.copy2      │  Yes   │    Yes    │   No  │      Yes       │
## │shutil.copyfileobj│   No   │     No    │  Yes  │       No       │
## └──────────────────┴────────┴───────────┴───────┴────────────────┘

## using shutil
import shutil

shutil.copy('test.txt.template', 'test__copy.txt')

shutil.copy2('test.txt.template', 'test__copy2.txt')

shutil.copyfile('test.txt.template', 'test__copyfile.txt')

## using shutil - copy file objects
f_src = open('test.txt.template', 'rb')
f_dest = open('test__copyfileobj.txt', 'wb')
shutil.copyfileobj(f_src, f_dest)
f_src.close()
f_dest.close()


## using os
import os

os.popen('cp test.txt.template test__os-popen.txt')

os.system('cp test.txt.template test__os-system.txt')


## using subprocess
## NB: setting 'shell=True' might be a security risk
import subprocess

status = subprocess.call('cp test.txt.template test__subprocess-call.txt', shell=True)

status = subprocess.check_output('cp test.txt.template test__subprocess-check_output.txt', shell=True)


print('READY.')
