#!/usr/bin/python
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2013-May-01

import sys
from os import path
from lxml import etree


def main(argv=sys.argv[1:]):
    if 0 == len(argv) or not path.isfile(argv[0]):
        print "usage: %s <path to .xml>" % sys.argv[0]
        sys.exit(1)
    xml=argv[0]

#    events=("start", "end")
#    for _, item in etree.iterparse( path.expanduser( path.expandvars( xml )), events=events):
#        print( "%s"%item.text)


    ## events like "start" and "end"
    for _, element in etree.iterparse( path.expanduser( path.expandvars( xml )), tag='CommandSetting'):
        print("%s" % (element.findtext('Name')) )


## start
if __name__ == '__main__':
    main()
    print "READY."
