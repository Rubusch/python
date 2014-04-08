#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-07
#
# DES is a symmetric block cipher cipher, it takes 64-bit blocks and encrypts
# with 56-bit keylength; since 1990 the algorithm is considered as being too
# weak against exhaustive key search attacks with just 56-bit keylength;
# further the origin and specific design of the S-boxes is not fully published,
# thus there might still be a chance to contain backdoors by designers
#
# this implementation is working on strings, which makes it easier readable or
# better to experience the algorithm, a better implementation would be to code
# it with hex numbers and bit operations directly

# TODO implement hexadecimal bit operations
# TODO implement blockwise en/decryption
# TODO change frontend
# TODO command line encryption
# TODO DBG()
# TODO clean up
# TODO refacture functions

import sys   # sys.exit()

### utils ###
def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def DBG(msg):
    print msg
    pass

def binstr(val, nbits):
#    print "val    %s"%bin(val)  
#    print "nbits  %s"%bin(nbits)  
    mask = 0x1 << nbits
#    print "mask = %s"%bin(mask)  
    ## add a mask to obtain leading 0s
    val += mask
#    print "val %s"%bin(val)  

    ## remove the 1 from the mask and return as string w/ leading 0s
#    print "bin(val)[:2] %s"%bin(val)[:2]  
#    print "bin(val)[3:] %s"%bin(val)[3:]  
    res = bin(val)[:2] + bin(val)[3:]
#    print "%s" % res  
    return res

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

# TODO refac
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

# TODO refac
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


class InitialPermutation():
    def __init__(self):
        self._blocksize = 64
# TODO hex numbers  
        self._initial_permutation=[58,50,42,34,26,18,10, 2,
                                   60,52,44,36,28,20,12, 4,
                                   62,54,46,38,30,22,14, 6,
                                   64,56,48,40,32,24,16, 8,
                                   57,49,41,33,25,17, 9, 1,
                                   59,51,43,35,27,19,11, 3,
                                   61,53,45,37,29,21,13, 5,
                                   63,55,47,39,31,23,15, 7]
# TODO hex numbers  
        self._final_permutation  =[40, 8,48,16,56,24,64,32,
                                   39, 7,47,15,55,23,63,31,
                                   38, 6,46,14,54,22,62,30,
                                   37, 5,45,13,53,21,61,29,
                                   36, 4,44,12,52,20,60,28,
                                   35, 3,43,11,51,19,59,27,
                                   34, 2,42,10,50,18,58,26,
                                   33, 1,41, 9,49,17,57,25]

    def _checklength(self, text):
        if self._blocksize != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(self._blocksize, len(text)))

    def _pick(self, text, position):
        return text[position-1]

    def initial_permutation(self, text):
        ## Note that both permutations do not increase the security of DES at all

#        self._checklength(text)  
#        return [self._pick(text,pos) for pos in self._initial_permutation]

        binlst = 0b0
        for pos in self._initial_permutation:
            val = (text >> (64 - ((pos-1)+1))) & 0b1
            binlst = (binlst <<1) | val
        return binlst


    def final_permutation(self, text):
        ## Note that both permutations do not increase the security of DES at all
        self._checklength(text)
        return [self._pick(text,pos) for pos in self._final_permutation]

class FeistelNetwork():
#    def __init__(self):
#        pass

    def _checklength(self, text, length):
        if length != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(length,len(text)))

    def round_xor(self, left, right):
        ## this step is NOT part of the f-function,
        ## it applies the encrypted half similar to a 'key' by xor-ing
        self._checklength(left, 32)
        self._checklength(right, 32)
        res = []
        for idx in range(len(left)):
            res += str(bin(int(left[idx]) ^ int(right[idx])))[2:]
        return res

    def round_merge_and_switch(self, left, right):
        ## this step is not part of the f-function,
        ## it merges both halfs, and twists left and right
        self._checklength(left,32)
        self._checklength(right,32)
        return right + left


class KeySchedule():
    def __init__(self, inputkey):
        ## the key schedule derives 16 round keys k[i], each consisting of
        ## 48 bits, from original 56-bit key; another term for round key is
        ## subkey
# TODO rm  
#        self._checklength(inputkey, 64) 
        self._rawinputkey = inputkey

# TODO hex values  
        self._pc1 = [57,49,41,33,25,17, 9, 1,
                     58,50,42,34,26,18,10, 2,
                     59,51,43,35,27,19,11, 3,
                     60,52,44,36,63,55,47,39,
                     31,23,15, 7,62,54,46,38,
                     30,22,14, 6,61,53,45,37,
                     29,21,13, 5,28,20,12, 4]
# TODO hex values  
        self._pc2 = [14,17,11,24, 1, 5, 3,28,
                     15, 6,21,10,23,19,12, 4,
                     26, 8,16, 7,27,20,13, 2,
                     41,52,31,37,47,55,30,40,
                     51,45,33,48,44,49,39,56,
                     34,53,46,42,50,36,29,32]

        self._shiftrules = []
        shift_one = [1,2,9,16]
        for pos in range(1,17):
            if pos in shift_one:
                self._shiftrules.append(1)
            else:
                self._shiftrules.append(2)
        DBG("init shiftrules: %s"%", ".join(map(str,self._shiftrules)))

        ## initial 1. PC-1 permutation, once at beginning (stripping last 8-bit)
        self._inputkey = self.pc1_permutation(self._rawinputkey)
        DBG("key schedule: 1. PC-1 permutation, stripping parity")

# TODO rm
#    def _checklength(self, text, length):
#        if length != len(text):
#            die("wrong blocksize passed, %d needed, %d passed"%(length,len(text)))
#
# TODO rm   
#    def _pick(self, text, position):
#        return text[position-1]

    def pc1_permutation(self, key):
        ## initial key permutation PC-1
        ## the 64-bit key is first reduced to 56 bits by ignoring every eighth
        ## bit, i.e. the parity bits are stripped in the initial PC-1
        ## permutation; again the parity bits certainly do not increase the key
        ## space! returns 56 bits
# TODO rm
#        self._checklength(key,64)   
#        return [self._pick(key,pos) for pos in self._pc1]   
#        DBG("key w/ parity  %s"%bin(key))   
        binlst = 0x0
        for pos in self._pc1:
            ## table entries start with 1, so reduce by 1
            val = (key >> (64 - ((pos-1)+1))) & 0b1 # TODO getnth_binary
            binlst = (binlst <<1)|val # TODO append binary
#        DBG("key w/o parity %s"%bin(binlst))  
        return binlst

#    def split(self, key):
    def splitkey(self, key):  
        ## the resulting 56-bit key is split into two halves C[0] and D[0], and
        ## the actual key schedule starts
        leftkey = (key >> 28) & 0xfffffff
        rightkey = key & 0xfffffff
        return leftkey, rightkey
#        return key[:28], key[28:]  

    def shift_left(self, key, roundidx):
        ## the two 28-bit halves are cyclically shifted left, i.e. rotated, by
        ## one or two bit positions depending on the round i according to the
        ## rules;
        ## note that the rotation takes only place within either the left or the
        ## right half; the total number of rotations sum up to 28 both halves
        ## are merged in this step
#        self._checklength(key,28) 
#        print "A \t\t%s"%bin(key)  
        shifter = self._shiftrules[roundidx]
#        print "shifter %d"%shifter  
        ret = (key << shifter) & 0xfffffff
        mask = 0x0
        for sh in range(shifter): mask = (mask<<1) | 0x1
        ret |= (key >> (28-shifter)) & mask
#        print "B \t\t%s"%bin(ret)  
        return ret
#        return key[shifter:] + key[:shifter]  

    def shift_right(self, key, roundidx):
        ## same as left shift, but used for decryption; in decryption round 1,
        ## subkey 16 is needed; in round 2 subkey 15
        ## in decryption round 1 the key is not rotated
        ## in decryption rounds 2,9 and 16 the two halves are rotated right by
        ## one bit
        ## in the other rounds, 3,4,5,6,7,8,10,11,12,13,14 and 15 the two halves
        ## are rotated right by two bits
        self._checklength(key,28)
        if 0 == roundidx: return key
        shifter = self._shiftrules[roundidx]
        keylen = len(key)
        return key[(keylen-shifter):] + key[:(keylen-shifter)]

    def pc2_permutation(self, key):
        ## to derive the 48-bit round keys k[i], the two halves are permuted
        ## bitwise again with PC-2, which stands for "permutation choice 2"
        ## PC-2 permutes the 56 input bits coming from C[i] and D[i] and ignores
        ## 8 of them; each bit is used in approximately 14 of the 16 round keys
#        self._checklength(key,56)  
        ## permute
        bitlst = 0x0
        for pos in self._pc2:
            ## key has 56 bit
            bitlst = DES._append(bitlst, DES._getnth(key, (pos-1), 56))
            ## bitlst has 48 bit
#        print "X %s"%bin(bitlst)  
        return bitlst
#        return [self._pick(key,pos) for pos in self._pc2]

    def get_encrypt_key(self, roundidx):
        ## generate a specific key for encryption
# TODO improve by generating all keys once, and putting them into a list - or explain why this was not done, but a repeted iteration
        ## the roundkey length is 56 bit
        ##
        ## iterate for each key until the roundidx is reached (easier to
        ## understand decryption afterwards)

        DBG( "key schedule: \tencrypt" )
        ## 1. PC-1 permutation, and cutting off parity bits - done by??
        key = self._inputkey
        for idx in range(roundidx+1):
            ## 2. split
            left, right = self.splitkey(key)
            DBG("key schedule: 2. split")
            DBG("key schedule: \tleft:   %s"%bin(left))
            DBG("key schedule: \tright:  %s"%bin(right))
#            printx(left,7) 
#            printx(right,7) 

            ## 3. shift left
            left = self.shift_left(left,idx)
            DBG("key schedule: 3. shift left")
            DBG("key schedule: \tleft:   %s"%bin(left))
#            printx(left,7) 
            right = self.shift_left(right,idx)
            DBG("key schedule: \tright:  %s"%bin(right))
#            printx(right,7) 

            ## 4. merge keys
#            key = left+right
            key = DES._append(left, right, 28)
            DBG("key schedule: 4. merge keys")
            DBG("key schedule: \tmerged: %s"%bin(key))
#            printx(key)

            ## 5. PC-2 permutation
            roundkey = self.pc2_permutation(key)
            DBG("key schedule: 5. PC-2 permutation")
            DBG("key schedule: \trndkey: %s"%bin(roundkey))
#            printx(roundkey)

        return roundkey


    def get_decrypt_key(self, roundidx):
#        print "\tdecrypt"
        ## generate keys for decryption, by the property
        ## C[0] == C[16] and D[0] == D[16]
        ## the first key for decryption is the last key for encryption
        key = self._inputkey
        for idx in range(roundidx+1):
            ## 2. split
            left, right = self.split(key)
#            printx(left,7)
#            printx(right,7)

            ## 3. shift right
            left = self.shift_right(left,idx)
#            printx(left,7)
            right = self.shift_right(right,idx)
#            printx(right,7)

            ## 4. merge keys
            key = left+right
#            printx(key)

            ## 5. PC-2 permutation
            roundkey = self.pc2_permutation(key)
#            printx(roundkey)

        return roundkey


class FFunction():
    def __init__(self, inputkey):
# TODO hex values  
        ## the e-box as other boxes as well, historically starts by one as first
        ## index; for a better understanding, this is kept throughtout the im-
        ## plemenetation
        self._ebox = [32, 1, 2, 3, 4, 5,
                       4, 5, 6, 7, 8, 9,
                       8, 9,10,11,12,13,
                      12,13,14,15,16,17,
                      16,17,18,19,20,21,
                      20,21,22,23,24,25,
                      24,25,26,27,28,29,
                      28,29,30,31,32, 1]

        ## S-boxes design criteria:
        ##
        ## 1. each S-box has six input bits and four output bits
        ## 2. no single output bit should be too close to a linear combination
        ##    of the input bits
        ## 3. if the lowest and the highest bits of the input are fixed and the
        ##    four middle bits are varied, each of the possible 4-bit output
        ##    values must occur exactly once
        ## 4. if two inputs to an S-box differ in exactly one bit, their outputs
        ##    must differ in at least two bits
        ## 5. if two inputs to an S-box differ in the two middle bits, their
        ##    outputs must differ in at least two bits
        ## 6. if two inputs to an S-box differ in their first two bits and are
        ##    identical in their last two bits, the two outputs must be
        ##    different
        ## 7. for any nonzero 6-bit difference between inputs, no more than 8 of
        ##    the 32 pairs of inputs exhibiting that difference may result in
        ##    the same output difference
        ## 8. a collision (zero output difference) at the 32-bit output of the
        ##    eight S-boxes is only possible for three adjacent S-boxes
# TODO hex values   
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

        self._keyschedule = KeySchedule(inputkey)

    def _checklength(self, text, length):
        if length != len(text):
            die("wrong blocksize passed, %d needed, %d passed"%(length,len(text)))

            
# TODO rm, refac!!
#    def _pick(self, text, position):
#        return text[position-1]

    def _sbox(self, text, sbox):
        ## text has 6 bit
#        self._checklength(text, 6)  
#        row = bin2dec(str(text[0]) + str(text[5]))
        val_first = (text >> 5) & 0x1
#        print "val_first %s"%bin(val_first) 
        val_last = text & 0x1
#        print "val_last  %s"%bin(val_last) 
        row = DES._append(val_first, val_last)
#        print "row (bin) %s"%bin(row)  
#        print "row %s"%binstr(row,2)  
#        col = bin2dec(str(text[1]) + str(text[2]) + str(text[3]) + str(text[4]))
        col = (text >> 1) & 0xf
#        print "col %s"%binstr(col,2)  
        ## 
# TODO why +16?
#        val = bin(sbox[row][col] + 16) # +16 only to keep the leading 0s, then val[3:] to cut of '0x1' again   
        return sbox[row][col]
#        print "val %s"%binstr(val,4)  
#        return str(val[3:]).upper()  

    def split(self, text):
        ## in round i it takes the right half R[i-1] of the output of the
        ## previous round and the current round key k[i] as input; the output of
        ## the f-function is used as an XOR-mask for encrypting the left half
        ## input bits L[i-1]

#        self._checklength(text,64)  
        left = (text>>32) & 0xffffffff
        right = text & 0xffffffff
        return (left, right)
#        return (text[:32],text[32:])  

    def expansion(self, text):
# TODO generic DES._permute(text, table), for 
# expansion(), pc2_permutation(), etc.   
        ## first, the 32-bit input is expanded to 48 bits by partitioning the
        ## input into eight 4-bit blocks and by expanding each block to 6 bits
        ## expand 32bit to 48bit
        
#        self._checklength(text,32)  
        # TODO _getnth(hexlst, nth, size) 
#        DES._getnth(text, pos) for pos in self._ebox) 
#        DES._append(hexlst, val, nbytes=1) 
#        print "A %#.8x"%text 
#        print "len ebox %d"%(len(self._ebox)/4)  
        bitlst = 0x0
        for pos in self._ebox:
            ## text has 32 bit
            bitlst = DES._append(bitlst, DES._getnth(text, (pos-1), 32))
        return bitlst
#        print "B %#.12x"%bitlst 
#        return [text[pos-1] for pos in self._ebox]  
#        return [self._pick(text,pos) for pos in self._ebox]   

    def encryptkey(self, text, roundidx):
        ## next, the 48-bit result of the expansion is XORed with the round key
        ## k[i], and the eight 6-bit blocks are fed into eight different
        ## substitution boxes, which are often referred to as S-boxes
#        self._checklength(text,48)  
#        key = self._keyschedule.get_encrypt_key(roundidx)  
        text ^= self._keyschedule.get_encrypt_key(roundidx)
        return text

#        self._checklength(key,48)  
#        ret = []
#        for idx in range(48):
#            ret.append(int(text[idx]) ^ int(key[idx]))
#        return ret

    def decryptkey(self, text, roundidx):
        ## same for decryption
        self._checklength(text,48)
        key = self._keyschedule.get_decrypt_key(roundidx)
        self._checklength(key,48)
        ret = []
        for idx in range(48):
            ret.append(int(text[idx]) ^ int(key[idx]))
        return ret


    def sbox(self, text):
        ## the s-boxes are the core of DES in terms of cryptographic strength;
        ## they are the only nonlinear element in the algorithm and provide
        ## confusion
#        self._checklength(text,48)  
        ret = []

        sub = (text >> (48 - 6)) & 0x3f  
        ret.append( self._sbox(sub, self._s1) )
#        ret.append( self._sbox(text[ 0: 6], self._s1) )

        
        die("XXX") 
        


        
        die("CCC")   
        
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
        ## finally, the 32-bit output is permuted bitwise according to the
        ## P permutation; unlike the initial IP and its inverse IP-1, the
        ## permutation P introduces diffusion because the four output bits of
        ## each S-box are permuted in such a way that they affect several
        ## different S-boxes in the following round
        self._checklength(text,32)
        return [self._pick(text,pos) for pos in self._pbox]


class DES():
    def __init__(self, inputkey):
        self._ip = InitialPermutation()

        self._ffunc = FFunction(inputkey)

        self._feistel = FeistelNetwork()

# TODO user  
    @staticmethod
    def _tablelookup(table, index, offset=0):
        ## params:
        ## table = table to look up content
        ## index = a 0xff value, where 0xf0 describes 16 row indexes and 0x0f
        ## 16 column indexes
        ##
        ## returns table value by the provided row and column indexes
        row = 0xf & (index >>(offset+4))
        if offset > 0:
            col = 0xf & (index >> offset)
        else:
            col = 0xf & index
        return table[row][col]

# TODO use  
    @staticmethod
#    def _getnth(hexlst, nth, size):
    def _getnth(bitlst, nth, size):
        ## params:
#        ## hexlst = a hex value, which serves as list of byte values  
#        ## nth = index of a specific byte in hexlst  
#        ## size = the full size of the hexlst in bytes  
#        ##
#        ## return the nth 8-bit number, contained in the hex list (a number)
        
        ## bitlst = a number, which serves as list of bit values
        ## nth = index of a specific bit in bitlst
        ## size = the full size of the bitlst in bits
        ##
        ## return the nth bit, contained in the bit list (a number)
        ## where nth is an index, starting with 0
# TODO rm, DES is bit based!
#        return ((hexlst >> (size - (nth+1)*8)) & 0xff)  
        return ((bitlst >> (size - (nth+1))) & 0x1)

# TODO use  
    @staticmethod
#    def _append(hexlst, val, nbytes=1):  
    def _append(bitlst, val, nbits=1):
#        ## appends an 8-bit hex val to a hex list (a number) of such values  
#        ## and returns it  
#        ##  
#        ## params:  
#        ## hexlst = a hex value, which serves as list of byte values  
#        ## val = a value e.g. as hex number to be appended  
#        ## nbytes = the number of bytes to be appended, the size of val  
#        return ((hexlst << (8*nbytes))|val)  
        
        ## appends a bit to a bit list (a number) of such values and returns it
        ##
        ## params:
        ## bitlst = a bit number, which serves as list of bit values
        ## val = a binary number to be appended
        ## nbits = the size of val
        ##         DES is a bit based algorithm, so the atomic unit is in bits
        return ((bitlst << nbits)|val)

    def encrypt(self, plaintext, ishex=False):
        ## params
        ## plaintext = the plaintext as string or as hex number
        ## ishex = if the plaintext was a hex number (True)

        ## init
        if ishex: state = plaintext
        else: state = int(plaintext.encode('hex'),16) & 0xffffffffffffffff
        DBG( "\n\nENCRYPTION\n\nplaintext: \t%#s"%bin(state) )

        ## initial permutation
        state = self._ip.initial_permutation(state)

        ## F-function
        for idx in range(16):
            ## DES loops the following steps
            ## 1. split
            left_half, right_half = self._ffunc.split(state)

            ## 2. expansion permutation E
            right_exp = self._ffunc.expansion(right_half)

            ## 3. key
            right_exp = self._ffunc.encryptkey(right_exp,idx)

            ## 4. s-boxes
            right_exp = self._ffunc.sbox(right_exp)



        
            die("BBB")  
        


            ## 5. permutation
            right_exp = self._ffunc.ppermute(right_exp)

            ## 6. merge left and right half
            state = self._feistel.round_xor(left_half, right_exp)

            ## 7. switch halves
            state = self._feistel.round_merge_and_switch(state, right_half)

        ## revert permutation
        return self._ip.final_permutation(state)

    def decrypt(self, ciphertext):
        ## initial permutation
        text = self._ip.initial_permutation(ciphertext)

        ## F-function
        for idx in range(16):
            ## DES loops the following steps
            ## 1. split
            ## in decryption, left and right halves are twisted!!!
            right_half, left_half = self._ffunc.split(text)

            ## 2. expansion permutation E
            right_exp = self._ffunc.expansion(right_half)

            ## 3. key
            right_exp = self._ffunc.decryptkey(right_exp,idx)

            ## 4. s-boxes
            right_exp = self._ffunc.sbox(right_exp)

            ## 5. permutation
            right_exp = self._ffunc.ppermute(right_exp)

            ## 6. merge left and right half
            text = self._feistel.round_xor(left_half, right_exp)

            ## 7. switch halves
            ## in decryption, left and right halves are twisted!!!
            text = self._feistel.round_merge_and_switch( right_half, text)

        ## revert permutation
        return self._ip.final_permutation(text)


### main ###
def main(argv=sys.argv[1:]):
    blocksize = 64 # TODO use   
    keysize_with_parity = 64
    inputkey = 0xffffffffffffffff   
    plaintext = ""
# TODO use  
    keylength = 256

    if len(argv) > 0:
        ## offer encryption by command line argument
        try:
            inputkey = int(argv[0],16)
            plaintext = argv[1]
        except:
            die('usage: either w/o arguments, or as follows\n$ %s <inputkey> "<plaintext>"\ne.g.\n$ %s %s "%s"'%(sys.argv[0],sys.argv[0],"0x000102030405060708090a0b0c0d0e0f","from Disco to Disco.."))
    else:
        ## init some raw input key example
        inputkey = 0x000102030405060708090a0b0c0d0e0f
        ## init some input text example
        plaintext = "jack and jill went up the hill to fetch a pail of water"
    
# TODO rm
#    inputkey = 0xffffffffffffffff   
    inputkey =  0x0000000000000080  
    plaintext = "Angelina"      
    

    print "initial key:\n%#.32x, key length %d, block size %d\n" % (inputkey, keylength, blocksize)

    print "plaintext:"
    print "%s\n" % plaintext

    ## init the algorithm
    des = DES(inputkey)

    ## some input text
    ## blocks
    ciphertext = []
    blocktext = ""
    for idx in range(len(plaintext)-1):
        blocktext += plaintext[idx]
        if idx % (blocksize/8) == 0:
            
            ciphertext.append(des.encrypt(blocktext))
            
            die("AAA")  
            
            blocktext = ""
    blocktext += plaintext[idx+1]
    ciphertext.append(des.encrypt(blocktext))

    ## print result
    print "encrypted:"
    for item in ciphertext:
        print "%#.32x"%item
    print "\n"

    ## decrypt
    decryptedtext = ""
    for block in ciphertext:
        decryptedtext += des.decrypt(block)

    ## print result
    print "decrypted:"
    print "%s\n" % decryptedtext


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
