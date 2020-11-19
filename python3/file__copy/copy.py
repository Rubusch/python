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

import shutil

shutil.copy('test.txt.template', 'test__copy.txt')

shutil.copy2('test.txt.template', 'test__copy2.txt')

shutil.copyfile('test.txt.template', 'test__copyfile.txt')

#shutil.copyfileobj('test.txt.template', 'test__copyfileobj.txt')  # copy file objects


print('READY.')
