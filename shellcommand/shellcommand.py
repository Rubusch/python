#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os
import subprocess

## get list output from command
cmd = 'svn ls https://svn.hqs.sbt.siemens.com/svn/ebuild/trunk'
repo_listing = [line.rstrip('\n') for line in os.popen( cmd )]
print repo_listing
print ''


## check return value
path_to_check = 'https://svn.hqs.sbt.siemens.com/svn/ebuild/trunk'
res = subprocess.call( ['svn', 'ls', path_to_check] )
print '\n\nres \'%s\'' % res

print "READY.\n"
