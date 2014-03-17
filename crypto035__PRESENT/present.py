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
            vals.append( bin2dec(elem) )
            elem = ""
        elem += str(binlist[idx])
    vals.append(bin2dec(elem))
    res = [str(hex(v)).upper()[2:] for v in vals]
    print "%s"%" ".join(map(str,res))


class Present:
    def __init__(self, inputkey):
        self._sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

        self._permutation = [ 0,16,32,48, 1,17,33,49, 2,18,34,50, 3,19,35,51,
                              4,20,36,52, 5,21,37,53, 6,22,38,54, 7,23,39,55,
                              8,24,40,56, 9,25,41,57,10,26,42,58,11,27,43,59,
                             12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]

    ## algorithm steps
    def _addRoundKey(self):
        pass

    def _sBoxLayer(self):
        pass

    def _pLayer(self):
        pass


    ## key schedule
    def _keyRegister(self):
        pass

    def _keyUpdate(self):
        pass


    ## public interface
    def encrypt(self, plaintext):
        for i in range(1,32):
            print "XXX ", plaintext  


    def decrypt(self, ciphertext):
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

    text = present.encrypt(text)

    die("STOP")   

    ## print result
    print "\n"
    print "encrypted:"
    printx(text)
    printhexlist(text)

    ## decrypt
    text = present.decrypt(text)

    ## print result
    print "\n"
    print "decrypted:"
    printx(text)
    printhexlist(text)


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
