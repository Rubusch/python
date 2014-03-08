#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-07
#
# the f-function introduces confusion and diffusion into the DES algorithm

import sys   # sys.argv[]

class FFunction():
    def __init__(self):
        self._ebox = [32, 1, 2, 3, 4, 5,
                       4, 5, 6, 7, 8, 9,
                       8, 9,10,11,12,13,
                      12,13,14,15,16,17,
                      16,17,18,19,20,21,
                      20,21,22,23,24,25,
                      24,25,26,27,28,29,
                      28,29,30,31,32, 1]

        self._s1 = [[14, 4,13, 1, 2,15,11, 8, 3,10, 6,12, 5, 9, 0, 7],
                    [ 0,15, 7, 4,14, 2,13, 1,10, 6,12,11, 9, 5, 3, 8],
                    [ 4, 1,14, 8,13, 6, 2,11,15,12, 9, 7, 3,10, 5, 0],
                    [15,12, 8, 2, 4, 9, 1, 7, 5,11, 3,14,10, 0, 6,13]]

        self._s2 = [[15, 1, 8,14, 6,11, 3, 4, 9, 7, 2,13,12, 0, 5,10],
                    [ 3,13, 4, 7,15, 2, 8,14,12, 0, 1,10, 6, 9,11, 5],
                    [ 0,14, 7,11,10, 4,13, 1, 5, 8,12, 6, 9, 3, 2,15],
                    [13, 8,10, 1, 3,15, 4, 2,11, 6, 7,12, 0, 5,14, 9]]

        self._s3 = [[10, 0, 9,14, 6, 3,15, 5, 1,13,12, 7,11, 4, 2, 8],
                    [13, 7, 0, 9, 3, 4, 6,10, 2, 8, 5,14,12,11,15, 1],
                    [13, 6, 4, 9, 8,15, 3, 0,11, 1, 2,12, 5,10,14, 7],
                    [ 1,10,13, 0, 6, 9, 8, 7, 4,15,14, 3,11, 5, 2,12]]

        self._s4 = [[ 7,13,14, 3, 0, 6, 9,10, 1, 2, 8, 5,11,12, 4,15],
                    [13, 8,11, 5, 6,15, 0, 3, 4, 7, 2,12, 1,10,14, 9],
                    [10, 6, 9, 0,12,11, 7,13,15, 1, 3,14, 5, 2, 8, 4],
                    [ 3,15, 0, 6,10, 1,13, 8, 9, 4, 5,11,12, 7, 2,14]]

        self._s5 = [[ 2,12, 4, 1, 7,10,11, 6, 8, 5, 3,15,13, 0,14, 9],
                    [14,11, 2,12, 4, 7,13, 1, 5, 0,15,10, 3, 9, 8, 6],
                    [ 4, 2, 1,11,10,13, 7, 8,15, 9,12, 5, 6, 3, 0,14],
                    [11, 8,12, 7, 1,14, 2,13, 6,15, 0, 9,10, 4, 5, 3]]

        self._s6 = [[12, 1,10,15, 9, 2, 6, 8, 0,13, 3, 4,14, 7, 5,11],
                    [10,15, 4, 2, 7,12, 9, 5, 6, 1,13,14, 0,11, 3, 8],
                    [ 9,14,15, 5, 2, 8,12, 3, 7, 0, 4,10, 1,13,11, 6],
                    [ 4, 3, 2,12, 9, 5,15,10,11,14, 1, 7, 6, 0, 8,13]]

        self._s7 = [[ 4,11, 2,14,15, 0, 8,13, 3,12, 9, 7, 5,10, 6, 1],
                    [13, 0,11, 7, 4, 9, 1,10,14, 3, 5,12, 2,15, 8, 6],
                    [ 1, 4,11,13,12, 3, 7,14,10,15, 6, 8, 0, 5, 9, 2],
                    [ 6,11,13, 8, 1, 4,10, 7, 9, 5, 0,15,14, 2, 3,12]]

        self._s8 = [[13, 2, 8, 4, 6,15,11, 1,10, 9, 3,14, 5, 0,12, 7],
                    [ 1,15,13, 8,10, 3, 7, 4,12, 5, 6,11, 0,14, 9, 2],
                    [ 7,11, 4, 1, 9,12,14, 2, 0, 6,10,13,15, 3, 5, 8],
                    [ 2, 1,14, 7, 4,10, 8,13,15,12, 9, 0, 3, 5, 6,11]]

        self._pbox = [16, 7,20,21,29,12,28,17,
                       1,15,23,26, 5,18,31,10,
                       2, 8,24,14,32,27, 3, 9,
                      19,13,30, 6,22,11, 4,25]

    def _checklength(self, text, length):
        if length != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(length,len(text)))

    def _pick(self, text, position):
        return text[position-1]

    def split(self, text):
        self._checklength(text,64)
        return (text[:32],text[32:])

    def expansion(self, text):
        self._checklength(text,32)
        ## expand 32bit to 48bit
        return [self._pick(text,pos) for pos in self._ebox]

    def _sbox(self, text, sbox):
        self._checklength(text, 6)
        row = dec(str(text[0]) + str(text[5]))
        col = dec(str(text[1]) + str(text[2]) + str(text[3]) + str(text[4]))
        val = bin(sbox[row][col] + 16)
        return str(val[3:]).upper()

    def sbox(self, text):
        self._checklength(text,48)
        ret = []
        ret.append( self._sbox(text[ 0: 6], self._s1) )
        ret.append( self._sbox(text[ 6:12], self._s2) )
        ret.append( self._sbox(text[12:18], self._s3) )
        ret.append( self._sbox(text[18:24], self._s4) )
        ret.append( self._sbox(text[24:30], self._s5) )
        ret.append( self._sbox(text[30:36], self._s6) )
        ret.append( self._sbox(text[36:42], self._s7) )
        ret.append( self._sbox(text[42:48], self._s8) )
        result = []
        for elem in ret:
            for char in elem:
                result.append(char)
        return result

    def ppermute(self, text):
        ## P permutation
        self._checklength(text,32)
        return [self._pick(text,pos) for pos in self._pbox]

    def xor(self, left, right):
        self._checklength(left, 32)
        self._checklength(right, 32)
        res = []
        for idx in range(len(left)):
            res += str(bin(int(left[idx]) ^ int(right[idx])))[2:]
        return res



### utils ###
def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def printx(text, cols=8):
    for idx in range(len(text)):
        if 0 == idx%cols:
            if idx != 0:
                print ""
        if int(text[idx]) < 10:
            print " %s "%text[idx],
        else:
            print "%s "%text[idx],
    print "\n"

def dec(string):
    val = 0
    for idx in reversed(range(len(string))):
        potence = 0
        if '1' == string[idx]:
            potence = 1
            for i in range(len(string)-1-idx):
                potence *= 2
        val += potence
    return val

def printhexlist(binlist):
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



### main ###
def main():
    ## init
    text = [1 for i in range(64)]
    ffunc = FFunction()

    ## DES loops the following steps
    ## 1. split
    left_half, right_half = ffunc.split(text)

    ## 2. expansion permutation E
    right_exp = ffunc.expansion(right_half)

    ## 3. key
    # TODO key schedule

    ## 4. s-boxes
    right_exp = ffunc.sbox(right_exp)

    ## 5. permutation
    right_exp = ffunc.ppermute(right_exp)

    ## 6. XOR left half to the right half
    text = ffunc.xor(left_half, right_exp)

    ## 7. switch halves
    # TODO switch left and right half, loop


    ## print result
    printhexlist(text)



### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
