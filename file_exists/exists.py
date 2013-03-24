#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os.path
import sys

if os.path.exists('./test.txt'):
    print "file exists, aborting"
    sys.exit(0)

print "file doesn't exist!\n"

print "READY.\n"


