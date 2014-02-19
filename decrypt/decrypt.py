#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Feb-18

import sys   # sys.argv[]
from os import path   # path.isfile()


## args - the filenmae
def main(argv=sys.argv[1:]):
    if 0 == len(argv) or not path.isfile(argv[0]):
        print "usage: %s <path to .txt>" % sys.argv[0]
        sys.exit(1)
    filename = argv[0]

    ## set up dictionary
    code = {}

    ## 1. figure out main frequencies, then
    ## 2. figure out missing letters more and more
    ## 3. in case there are typos ;)
    ## all lowercase
    code.update({'a':'X'})
    code.update({'b':'T'})
    code.update({'c':'W'})
    code.update({'d':'D'}) #?
    code.update({'e':'V'}) #?
    code.update({'f':'Q'})
    code.update({'g':'Z'})
    code.update({'h':'L'}) #?
    code.update({'i':'S'}) #!
    code.update({'j':'O'}) #!
    code.update({'k':'N'})
    code.update({'l':'B'}) #?
    code.update({'m':'A'})
    code.update({'n':'U'})
    code.update({'o':'G'}) #?
    code.update({'p':'H'}) #!
    code.update({'q':'K'})
    code.update({'r':'E'})
    code.update({'s':'P'}) #?
    code.update({'t':'Y'}) #?
    code.update({'u':'R'}) #?
    code.update({'v':'C'})
    code.update({'w':'I'})
    code.update({'x':'F'}) #!
    code.update({'y':'M'}) #?
#    code.update({'z':''}) # not used


    ## read text
    f=open(filename)
    cnt=0
    for line in f:

    ## substitute
        result = "".join([code[i] if i in code else i  for i in line])

    ## display result
        print "%d:\t%s"%(cnt,result),
        cnt+=1
    f.close()


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
