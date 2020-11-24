#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-05

import sys
from os import path

class Bid():
    def __init__(self, user, money, time):
        self.user = user
        self.money = money
        self.time = time
    # TODO 
        
class Auction():
    def __init__(self, filename):
        self.bids = []
        self.initbids(filename)

    def initbids(self, filename):
        ## read file, parse and init list of bids
        f=open(filename)
        while( True ):
            line = f.readline()
            # TODO check EOF
            # TODO update "file_read" example
            if '' == line: break   

            ## parsing
            ## e.g.
            ## <span>EUR&nbsp;1,00</span></td><td class="contentValueFont" align="left"><div><span>20.02.14    </span><span style="white-space:nowrap;">20:59:29 MEZ</span></div></td><td class="emptyCellPadding"><img src="eBay%20Deutschland%20Gebots%C3%BCbersicht_files/s.gif" alt=" " height="1" width="1"></td></tr><tr id="viznobrd"><td class="emptyCellPadding" width="1"><img src="eBay%20Deutschland%20Gebots%C3%BCbersicht_files/s.gif" alt=" " height="1" width="1"></td><td class="newcontentValueFont">Startpreis</td><td class="contentValueFont" style="color:#666" align="left" nowrap="nowrap">&nbsp;&nbsp;


            ## parse user
            ## parse money
            ## parse time

            print "XXX '%s'"%line  

        die("STOP")   


        ## then... f.close()
        # TODO 

    def printgraph(self):
        # TODO
        pass


def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def main(argv=sys.argv[1:]):
    ## pass args as path
    if 0 == len(argv) or not path.isfile(argv[0]):
        die("usage: %s <path to .html>" % sys.argv[0])

    ## read file
    auction = Auction(argv[0])

    ## do output, etc...
    # TODO

### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
