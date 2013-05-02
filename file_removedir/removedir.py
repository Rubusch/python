#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

import os
import re


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

if os.path.exists( './folder' ):
    print "delete file and folder"
    # remove "folder" in "./"
    regex = re.compile('folder')
    rmpattern( './', regex)

else:
    print "create file and folder"
    # create "./folder" and "./folder/test.txt"
    os.mkdir( './folder' )
    FILE = open('./folder/test.txt', 'w')
    FILE.write(text)
    FILE.close()

print "READY.\n"

