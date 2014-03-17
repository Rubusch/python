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
#
# PRESENT exists as PRESENT-80 or -128 with corresponding key length
# PRESENT is based on a substitution-permutation-network

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

def dec2bin(dec, bits=8):
    ## generate bin from decimal value, return a list of bits length
    if dec > 2**bits-1: die("ERROR: dec2bin, dec is too big for number of bits")
    binlst = []
    dec = int(dec)
    for exp in reversed(range(bits)):
        subt = 2 ** exp
        if subt <= dec:
            dec-=subt
            binlst.append(1)
        else:
            binlst.append(0)
    return binlst

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
        
        # self._sbox = [[1,1,0,0], # 12
        #               [0,1,0,1], #  5
        #               [0,1,1,0], #  6
        #               [1,0,1,1], # 11
        #               [1,0,0,1], #  9
        #               [0,0,0,0], #  0
        #               [1,0,1,0], # 10
        #               [1,1,0,1], # 13
        #               [0,0,1,1], #  3
        #               [1,1,1,0], # 14
        #               [1,1,1,1], # 15
        #               [1,0,0,0], #  8
        #               [0,1,0,0], #  4
        #               [0,1,1,1], #  7
        #               [0,0,0,1], #  1
        #               [0,0,1,0]] #  2
        self._sbox = [0xc,0x5,0x6,0xb,0x9,0x0,0xa,0xd,0x3,0xe,0xf,0x8,0x4,0x7,0x1,0x2]
        self._sbox_inv = [self._sbox.index(i) for i in xrange(len(self._sbox))]

        self._permutation = [ 0,16,32,48, 1,17,33,49, 2,18,34,50, 3,19,35,51,
                              4,20,36,52, 5,21,37,53, 6,22,38,54, 7,23,39,55,
                              8,24,40,56, 9,25,41,57,10,26,42,58,11,27,43,59,
                             12,28,44,60,13,29,45,61,14,30,46,62,15,31,47,63]
        self._permutation_inv = [self._permutation.index(i) for i in xrange(len(self._permutation))]

        ## init all 31 keys once, then just go by index
        self._roundkeys = []

        self._generateRoundkeys80(inputkey)

    ## utilities
    def _checklength(self, text, length):
        if length != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(length,len(text)))

    def _xor(self, binlst1, binlst2):
        self._checklength( binlst1, len(binlst2))
        return [int(binlst1[idx])^int(binlst2[idx]) for idx in range(len(binlst1))]

    ## algorithm steps
    def _generateRoundkeys80(self, inputkey):

        print "%#x" % inputkey

#        self._checklength(inputkey, 80)
        key = inputkey
        for idx in xrange(1,32):
            ## cut out first 64 bit as round key
#            self._roundkeys.append(key[:64]) 
            self._roundkeys.append(key >> 16)

            ## left shift by 61 bit
#            key = key[61:] + key[:61] 
            key = ((key & (2**19-1))<<61) + (key>>19)

            ## S(key[0])
#            key[0:4] = self._sBox(key[0:4]) 
            key = (self._sbox[key >> 76]  << 76) + (key & (2**76-1))
            ## key[60:65] XOR roundCounter
#            key[60:65] = self._xor(key[60:65], dec2bin(idx,5)) 
            key ^= idx << 15

# TODO  
    def _generateRoundkeys128(self, inputkeys):
        self._checklength(inputkey, 128)
        key = inputkey
        for idx in xrange(1,32):
            ## cut out first 64 bit as round key
#            self._roundkeys.append(key[:64]) 
            self._roundkeys.append(key >> 64)    

            ## left shift by 61 bit
#            key = key[61:] + key[:61] 
            key = ((key & (2**67-1))<<61) + (key>>67)

            ## S(key[0])
#            key[0:4] = self._sBox(key[0:4]) 
            key = (self._sbox[key >> 124]  << 124) + (self._sbox[(key>>120) & 0xf] << 120) + (key & (2**120-1))
            ## key[60:65] XOR roundCounter
#            key[60:65] = self._xor(key[60:65], dec2bin(idx,5)) 
            key ^= idx << 62


    def _addRoundKey(self, state, key):
        self._checklength(state, len(key))
        return [int(state[idx])^int(key[idx]) for idx in range(len(key))]

    def _sBoxLayer(self, state):
        self._checklength(state, 64)
        for idx in range(16):
            state[idx*4:idx*4+4] = self._sBox(state[idx*4:idx*4+4])
        return state

    def sBoxLayer_dec(self, state):
        
        pass

    def _pLayer(self, state):
        self._checklength(state, 64)
        ret = [0 for i in range(64)]
        for idx in range(len(state)):
            ret[self._permutation[idx]] = state[idx]
        return ret

    def _pLayer_dec(self, state):
        
        pass

    ## S-box tools
    def _sBox(self, fourbit):
        self._checklength(fourbit,4)
        return self._sbox[bin2dec("".join(map(str,fourbit)))]

    ## public interface
    def encrypt(self, plaintext):
        self._checklength( plaintext, 64) # check for blocksize
        state = [i for i in plaintext]
        for idx in range(31):

#            key = self._roundkeys[idx]
#            state = self._addRoundKey(state, key)

            state = self._sBoxLayer(state)
            state = self._pLayer(state)
        return state

    def decrypt(self, ciphertext):
        self._checklength( ciphertext, 64) # check for blocksize
        state = [i for i in ciphertext]
        for idx in reversed(range(31)):
#            print idx

#            key = self._roundkeys[idx]
#            state = self._addRoundKey(state, key)

            state = self._pLayer_dec(state)

            die("STOP")   

            state = self._sBoxLayer_dec(state)
        return state

### main ###
def main():
    ## init
    blocksize = 64
    keysize = 80
    ## some raw input key
#    inputkey = [0 for i in range(keysize)] # all zeros
    inputkey = 0xbbbb55555555eeeeffff

    
    # inputkey = [1,0,1,1, 1,0,1,1, 1,0,1,1, 1,0,1,1,
    #             0,1,0,1, 0,1,0,1, 0,1,0,1, 0,1,0,1,
    #             0,1,0,1, 0,1,0,1, 0,1,0,1, 0,1,0,1,
    #             1,1,1,0, 1,1,1,0, 1,1,1,0, 1,1,1,0,
    #             1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1]
    # printhexlist(inputkey)  
    
#    for idx in range(40): inputkey[idx] = 1 # some ones
#    inputkey[0] = 1 # just set one 1
    print "initial key:"
    print "%#x" % inputkey
#    printhexlist(inputkey) 

    ## init the PRESENT-80
    present = Present(inputkey)

    die("STOP")

    ## some input text
#    text = [0 for i in range(blocksize)] ## all zeros
#    text[0] = 1 # set one
    text = 0x8000000000000000

    print "plaintext:"
    print "%#x" % text
#    printx(text)
#    printhexlist(text)

    text = present.encrypt(text)

    ## print result
    print "\n"
    print "encrypted:"
#    printx(text)
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
