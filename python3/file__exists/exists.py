#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

import os.path
import sys

class ABC():
    pass

try:
    if os.path.exists('./test.txt'):
        print("file exists, ok")
        raise ABC

    print("file doesn't exist, fail!\n")

except ABC as e:
    print("READY.\n")


