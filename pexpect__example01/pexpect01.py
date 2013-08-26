#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-August-25
#
# RESOURCES:
# http://www.noah.org/wiki/pexpect
# http://dbudwm.wordpress.com/2011/08/21/pexpect-kommandozeilenprogramme-mit-python-steuern/
#
# in case install pexpect locally e.g.
# python setup.py install --prefix=/home/lothar/
# and set PYTHONPATH=${PYTHONPATH}:/home/lothar/lib/site-packages/
#
# NOTE: the default PYTHONPATH will be ALWAYS prepended by sys.path

import pexpect

#child = pexpect.spawn("ls -la /")
child = pexpect.spawn("echo 'Enter Password:'")
while True:
    i = child.expect([ pexpect.EOF, 'Enter Password:'], timeout = None)
    if i == 1:
        print "asked for password, do pexpect.sendline()"
    elif i == 0:
        print "--Ende--"
        break


