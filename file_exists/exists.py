#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

import os.path
import sys

if os.path.exists('./test.txt'):
    print "file exists, aborting"
    sys.exit(0)

print "file doesn't exist!\n"

print "READY.\n"


