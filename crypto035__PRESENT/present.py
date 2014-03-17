#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-17
#
# a lightweight block cipher, designed specifically for applications such as
# RFID tags or other pervasive computing applications that are extremely power
# or cost constrained
# [p. 78, Understanding Cryptography, Christof Paar, Jan Pelzl, 2010, Springer]

import sys   # sys.argv[]

### utils ###
def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def bin2dec(binstr):
    ## generate decimal value from binary string
    val = 0
    for idx in reversed(range(len(binstr))):
        potence = 0
        if '1' == binstr[idx]:
            potence = 1
            for i in range(len(binstr)-1-idx):
                potence *= 2
        val += potence
    return val

def printx(text, cols=8):
    ## print in columns
    for idx in range(len(text)):
        if 0 == idx%cols:
            if idx != 0:
                print ""
        if int(text[idx]) < 10:
            print " %s "%text[idx],
        else:
            print "%s "%text[idx],
    print "\n"

def printhexlist(binlist):
    ## print binary value list, as hex values
    elem = ""
    vals = []
    for idx in range(len(binlist)):
        if 0 == idx%4 and idx != 0:
            vals.append( dec(elem) )
            elem = ""
        elem += str(binlist[idx])
    vals.append(dec(elem))
    res = [str(hex(v)).upper()[2:] for v in vals]
    print "%s"%" ".join(map(str,res))


class Present:
    def __init__(self):
        pass

### main ###
def main():
    ## init
    blocksize = 64
    keysize = 80
    ## some raw input key
    inputkey = [0 for i in range(keysize)] # all zeros
#    for idx in range(16): inputkey[idx] = 1 # some ones
#    inputkey[0] = 1 # just set one 1

    ## init the PRESENT-80
    present = Present(inputkey)

    ## some input text
    text = [0 for i in range(blocksize)] ## all zeros
    text[0] = 1 # set one

    print "initial:"
    printx(text)
    printhexlist(text)

    text = des.encrypt(text)

    ## print result
    print "\n"
    print "encrypted:"
    printx(text)
    printhexlist(text)

    ## decrypt
    text = des.decrypt(text)

    ## print result
    print "\n"
    print "decrypted:"
    printx(text)
    printhexlist(text)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
