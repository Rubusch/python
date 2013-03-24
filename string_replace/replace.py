#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

val = "asdf-1.2.3"
print "val '%s'" % val

## replace '.' by '_'
import string
print "val '%s'" % string.replace( val, '.', '_')


print "READY.\n"
