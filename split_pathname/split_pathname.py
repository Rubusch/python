#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os

mesg = 'sys-kernel/eboard-source/eboard-source-2.6.32.18.ebuild'
print 'message' 
print mesg
print ''

print 'cut off the last filename'
print mesg.rsplit( '/', 1)[0]
print ''

print 'cut off the last filename'
print os.path.dirname( mesg )
print ''

print "READY.\n"
