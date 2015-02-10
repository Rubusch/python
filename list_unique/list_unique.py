#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01



def out( mesg, item_list ):
    print mesg
    for item in item_list: print item
    print ''


arr = [ 'a', 'b', 'c' ]
out( '1. vanilla', arr )

arr.append( 'a' )
out( '2. append a', arr )

arr = set( arr )
out( '3. unique', arr )

print 'READY.\n'

