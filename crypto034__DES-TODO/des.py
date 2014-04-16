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

DBG_PRINT_HEX = True
def tostring(val, nbits):
    ## binary representation
    mask = 0x1 << nbits
    val += mask

    if DBG_PRINT_HEX:
        ## hexadecimal representation
        res = ("%#.x"%val)[:2] + ("%#.x"%val)[3:]
    else:
        ## remove the 1 from the mask and return as string w/ leading 0s
        res = bin(val)[:2] + bin(val)[3:]
    return res

class InitialPermutation():
    def __init__(self):
        self._blocksize = 64
#        self._initial_permutation=[0x3a,0x32,0x2a,0x22,0x1a,0x12,0x0a,0x02,
#                                   0x3c,0x34,0x2c,0x24,0x1c,0x14,0x0c,0x04,
#                                   0x3e,0x36,0x2e,0x26,0x1e,0x16,0x0e,0x06,
#                                   0x40,0x38,0x30,0x28,0x20,0x18,0x10,0x08,
#                                   0x39,0x31,0x29,0x21,0x19,0x11,0x09,0x01,
#                                   0x3b,0x33,0x2b,0x23,0x1b,0x13,0x0b,0x03,
#                                   0x3d,0x35,0x2d,0x25,0x1d,0x15,0x0d,0x05,
#                                   0x3f,0x37,0x2f,0x27,0x1f,0x17,0x0f,0x07]
# TODO rm, or leave in decimal?
        ## starts with 1
        self._initial_permutation=[58,50,42,34,
                                   26,18,10, 2,
                                   60,52,44,36,
                                   28,20,12, 4,
                                   62,54,46,38,
                                   30,22,14, 6,
                                   64,56,48,40,
                                   32,24,16, 8,
                                   57,49,41,33,
                                   25,17, 9, 1,
                                   59,51,43,35,
                                   27,19,11, 3,
                                   61,53,45,37,
                                   29,21,13, 5,
                                   63,55,47,39,
                                   31,23,15, 7]

# TODO hex numbers  
        ## starts with 1
        self._final_permutation  =[40, 8,48,16,
                                   56,24,64,32,
                                   39, 7,47,15,
                                   55,23,63,31,
                                   38, 6,46,14,
                                   54,22,62,30,
                                   37, 5,45,13,
                                   53,21,61,29,
                                   36, 4,44,12,
                                   52,20,60,28,
                                   35, 3,43,11,
                                   51,19,59,27,
                                   34, 2,42,10,
                                   50,18,58,26,
                                   33, 1,41, 9,
                                   49,17,57,25]


class KeySchedule():
    def __init__(self, inputkey):

# TODO hex values  
        ## starts with 1
        self._pc1 = [57,49,41,33,
                     25,17, 9, 1,
                     58,50,42,34,
                     26,18,10, 2,
                     59,51,43,35,
                     27,19,11, 3,
                     60,52,44,36,
                     63,55,47,39,
                     31,23,15, 7,
                     62,54,46,38,
                     30,22,14, 6,
                     61,53,45,37,
                     29,21,13, 5,
                     28,20,12, 4]
# TODO hex values  
        ## starts with 1
        self._pc2 = [14,17,11,24,
                      1, 5, 3,28,
                     15, 6,21,10,
                     23,19,12, 4,
                     26, 8,16, 7,
                     27,20,13, 2,
                     41,52,31,37,
                     47,55,30,40,
                     51,45,33,48,
                     44,49,39,56,
                     34,53,46,42,
                     50,36,29,32]

        self._shiftrules = []
        shift_one = [1,2,9,16]
        for pos in range(1,17):
            if pos in shift_one:
                self._shiftrules.append(1)
            else:
                self._shiftrules.append(2)
        DBG("key schedule: init shiftrules: %s"%", ".join(map(str,self._shiftrules)))

        ## key expansion
        ##
        ## the key schedule derives 16 round keys k[i], each consisting of
        ## 48 bits, from original 56-bit key; another term for round key is
        ## subkey
        self._encryptkeys = self._encrypt_key_expansion(inputkey)

        ## decryption keys are the same as encyrption keys, but also can be gene-
        ## rated by using a right shift instead of a left shift, so here is pre-
        ## sented how to generate them freshly, instead of accessing the already
        ## generated keys with the corresponding reverted index which of course
        ## would be the efficient way how to do it
        self._decryptkeys = self._decrypt_key_expansion(inputkey)

    def _encrypt_key_expansion(self, inputkey):
        DBG("\nkey schedule: encryption key expansion")
        DBG("key schedule: init key %s"%tostring(inputkey, 64))
        ## initial 1. PC-1 permutation, once at beginning (stripping last 8-bit)
        ##
        ## the 64-bit key is first reduced to 56 bits by ignoring every eighth
        ## bit, i.e. the parity bits are stripped in the initial PC-1
        ## permutation; again the parity bits certainly do not increase the key
        ## space! returns 56 bits
        stripped_initkey = DES._map_by_table(inputkey, self._pc1, 64)
        DBG("key schedule: 1. PC-1 permutation, stripping parity")
        DBG("key schedule: key      %s"%tostring(stripped_initkey, 56))

        ## generate a specific key for encryption
        ## the roundkey length is 56 bit
        ##
        ## iterate for each key until the roundidx is reached (easier to
        ## understand decryption afterwards)
        DBG( "key schedule" )
        keys = []
        key = stripped_initkey

        for idx in range(16):
            ## 2. split
            left, right = self._splitkey(key)
            DBG("key schedule: 2. split")
            DBG("key schedule: key       %s %s"%(tostring(left, 28), tostring(right, 28)))

            ## 3. shift left
            left = self._shiftleft(left, idx)
            right = self._shiftleft(right, idx)
            DBG("key schedule: 3. shift left")
            DBG("key schedule: key       %s %s"%(tostring(left, 28), tostring(right, 28)))

            ## 4. merge keys
            key = DES._append(left, right, 28)
            DBG("key schedule: 4. merge keys")
            DBG("key schedule: key       %s"%(tostring(key, 56)))

            ## 5. PC-2 permutation
            roundkey = self.pc2_permutation(key)
            DBG("key schedule: 5. PC-2 permutation")
            DBG("key schedule: rnd key   %s"%(tostring(roundkey, 48)))

            keys.append(roundkey)
        return keys

    def _decrypt_key_expansion(self, inputkey):
        DBG("\nkey schedule: decryption key expansion")
        DBG("key schedule: init key %s"%tostring(inputkey, 64))

        stripped_initkey = DES._map_by_table(inputkey, self._pc1, 64)
        DBG("key schedule: 1. PC-1 permutation, stripping parity")
        DBG("key schedule: key      %s"%tostring(stripped_initkey, 56))

        DBG( "key schedule" )
        keys = []
        key = stripped_initkey

        for idx in range(16):
            ## 2. split
            left, right = self._splitkey(key)
            DBG("key schedule: 2. split")
            DBG("key schedule: key       %s %s"%(tostring(left, 28), tostring(right, 28)))
# TODO check value

            ## 3. shift right
            left = self._shiftright(left, idx) # FIXME implementation  
            right = self._shiftright(right, idx) # FIXME  
            DBG("key schedule: 3. shift right")
            DBG("key schedule: key       %s %s"%(tostring(left, 28), tostring(right, 28)))

#            die("XXX")  

            ## 4. merge keys
            key = DES._append(left, right, 28)
            DBG("key schedule: 4. merge keys")
            DBG("key schedule: key       %s"%(tostring(key, 56)))

            ## 5. PC-2 permutation
            roundkey = self.pc2_permutation(key)
            DBG("key schedule: 5. PC-2 permutation")
            DBG("key schedule: rnd key   %s"%(tostring(roundkey, 48)))

            keys.append(roundkey)
        return keys

        
        ## generate keys for decryption, by the property
        ## C[0] == C[16] and D[0] == D[16]
        ## the first key for decryption is the last key for encryption
#        key = self._inputkey 
#        for idx in range(roundidx+1): 
#            ## 2. split 
#            left, right = self._splitkey(key) 
# 
# 
#            ## 3. shift right
#            left = self._shiftright(left,idx)
#            right = self._shiftright(right,idx)
#
#
#            ## 4. merge keys
#            key = left+right
#
#
#            ## 5. PC-2 permutation
#            roundkey = self.pc2_permutation(key)
#
#
#        return roundkey
        
        # TODO
        return keys

    def _splitkey(self, key):
        ## the resulting 56-bit key is split into two halves C[0] and D[0], and
        ## the actual key schedule starts
        leftkey = (key >> 28) & 0xfffffff
        rightkey = key & 0xfffffff
        return leftkey, rightkey

    def _shiftleft(self, key, roundidx):
        ## the two 28-bit halves are cyclically shifted left, i.e. rotated, by
        ## one or two bit positions depending on the round i according to the
        ## rules;
        ## note that the rotation takes only place within either the left or the
        ## right half; the total number of rotations sum up to 28 both halves
        ## are merged in this step
        ## key has size of 28 bit, result has 28 bit
        
        shifter = self._shiftrules[roundidx]
        ret = (key <<shifter) & 0xfffffff
        mask = 0x0
        for sh in range(shifter): mask = (mask<<1) | 0x1
        ret |= (key >>(28-shifter)) & mask
        return ret

    def _shiftright(self, key, roundidx):
        ## same as left shift, but used for decryption; in decryption round 1,
        ## subkey 16 is needed; in round 2 subkey 15
        ## in decryption round 1 the key is not rotated
        ## in decryption rounds 2,9 and 16 the two halves are rotated right by
        ## one bit
        ## in the other rounds, 3,4,5,6,7,8,10,11,12,13,14 and 15 the two halves
        ## are rotated right by two bits
        ## key has size of 28 bit, result has 28 bit

# TODO size?
        
#        key = 0x8000000
#        key = 0xf0f0f0f
#        DBG("X key     %s"%tostring(key, 28))  
#        roundidx = 1
        

        ## special for decryption, and key generation
        if 0 == roundidx: return key
        shifter = self._shiftrules[roundidx]
        ret = 0x0
        for bit in range(shifter):
            ret = DES._append(ret, (key & 0x1))
            key >>= 1

        ret = DES._append(ret, key, (28-shifter))
        return ret

    def pc2_permutation(self, key):
        ## to derive the 48-bit round keys k[i], the two halves are permuted
        ## bitwise again with PC-2, which stands for "permutation choice 2"
        ## PC-2 permutes the 56 input bits coming from C[i] and D[i] and ignores
        ## 8 of them; each bit is used in approximately 14 of the 16 round keys
        ## key has 56-bit size, result has 48-bit size
        binlst = 0x0
        for pos in self._pc2:
            binlst = DES._append(binlst, DES._getnth(key, (pos-1), 56))
        return binlst

## TODO rm
#    def get_encrypt_key(self, roundidx):
#        ## generate a specific key for encryption
#        ## the roundkey length is 56 bit
#        ##
#        ## iterate for each key until the roundidx is reached (easier to
#        ## understand decryption afterwards)
#        return self._encryptkeys[roundidx]
#
#    def get_decrypt_key(self, roundidx):
#        return self._decryptkeys[roundidx]


class FFunction():
    def __init__(self, inputkey):
        ## the e-box as other boxes as well, historically starts by one as first
        ## index; for a better understanding, this is kept throughtout the im-
        ## plemenetation

        ## starts with 1
        self._ebox = [32, 1, 2, 3,
                       4, 5, 4, 5,
                       6, 7, 8, 9,
                       8, 9,10,11,
                      12,13,12,13,
                      14,15,16,17,
                      16,17,18,19,
                      20,21,20,21,
                      22,23,24,25,
                      24,25,26,27,
                      28,29,28,29,
                      30,31,32, 1]

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

        ## starts with 1
        self._pbox = [16, 7,20,21,
                      29,12,28,17,
                       1,15,23,26,
                       5,18,31,10,
                       2, 8,24,14,
                      32,27, 3, 9,
                      19,13,30, 6,
                      22,11, 4,25]

        self._keyschedule = KeySchedule(inputkey)

    def _sbox(self, text, sbox):
        ## text has 6 bit, result is a 4-bit s-box entry
        val_first = (text >> 5) & 0x1
        val_last = text & 0x1
        row = DES._append(val_first, val_last)
        col = (text >> 1) & 0xf
        return sbox[row][col]

    def split(self, text):
        ## in round i it takes the right half R[i-1] of the output of the
        ## previous round and the current round key k[i] as input; the output of
        ## the f-function is used as an XOR-mask for encrypting the left half
        ## input bits L[i-1]
        ## takes 64-bit text, and splits into two 32-bit pieces
        left = (text>>32) & 0xffffffff
        right = text & 0xffffffff
        return (left, right)

    def expansion(self, text):
# TODO generic DES._permute(text, table), for 
# expansion(), pc2_permutation(), etc.   
        ## first, the 32-bit input is expanded to 48 bits by partitioning the
        ## input into eight 4-bit blocks and by expanding each block to 6 bits
        ## expand 32bit to 48bit
        binlst = 0x0
        for pos in self._ebox:
            ## text has 32 bit
            binlst = DES._append(binlst, DES._getnth(text, (pos-1), 32))
        return binlst

    def encryptkey(self, text, roundidx):
        ## next, the 48-bit result of the expansion is XORed with the round key
        ## k[i], and the eight 6-bit blocks are fed into eight different substi-
        ## tution boxes, which are often referred to as S-boxes takes a 48-bit
        ## input and a 48-bit key, the result then is 48-bit
        DBG("\t\t\t\t\t | %s - roundkey[%d]"%(tostring(self._keyschedule._encryptkeys[roundidx], 48), roundidx))
#        text ^= self._keyschedule.get_encrypt_key(roundidx)  
        text ^= self._keyschedule._encryptkeys[roundidx]
        return text

    def decryptkey(self, text, roundidx):
        DBG("\t\t\t\t\t | %s - roundkey[%d]"%(tostring(self._keyschedule._decryptkeys[roundidx], 48), roundidx))
#        text ^= self._keyschedule.get_decrypt_key(roundidx)  
        text ^= self._keyschedule._decryptkeys[roundidx]
        return text

    def sbox(self, text):
        ## the s-boxes are the core of DES in terms of cryptographic strength;
        ## they are the only nonlinear element in the algorithm and provide
        ## confusion
        ## takes a 48-bit input, result is 32-bit
        ##
        ## this is because the 6-bit sequences taken for obtaining the s-box
        ## entries are converted 8 times into 4-bit s-box table entries each
        binlst = 0x0
        sub = (text >> (48 - 6)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s1), 4)

        sub = (text >> (48 - 12)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s2), 4)

        sub = (text >> (48 - 18)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s3), 4)

        sub = (text >> (48 - 24)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s4), 4)

        sub = (text >> (48 - 30)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s5), 4)

        sub = (text >> (48 - 36)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s6), 4)

        sub = (text >> (48 - 42)) & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s7), 4)

        sub = text & 0x3f
        binlst = DES._append(binlst, self._sbox(sub, self._s8), 4)

        return binlst

class DES():
    def __init__(self, inputkey):
        self._ip = InitialPermutation()
        self._ffunc = FFunction(inputkey)

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

    @staticmethod
    def _getnth(binlst, nth, size):
        ## return the nth bit, contained in the bit list (a number)
        ## where nth is an index, starting with 0
        ##
        ## params:
        ## binlst = a number, which serves as list of bit values
        ## nth = index of a specific bit in binlst
        ## size = the full size of the binlst in bits
        return ((binlst >> (size - (nth+1))) & 0x1)

    @staticmethod
    def _append(binlst, val, nbits=1):
        ## appends a bit to a bit list (a number) of such values and returns it
        ##
        ## params:
        ## binlst = a bit number, which serves as list of bit values
        ## val = a binary number to be appended
        ## nbits = the size of val
        ##         DES is a bit based algorithm, so the atomic unit is in bits
        return ((binlst << nbits)|val)

    @staticmethod
    def _map_by_table(text, table, textsize):
        ## fetches a refered bit from text and maps it according to the table
        ##
        ## params:
        ## text = the input text, a bit number
        ## table = the mapping table
        ## textsize = the number of bits for text
        binlst = 0b0
        for pos in table:
            ## fetch bit specified by table
            val = (text >> (textsize - ((pos-1)+1))) & 0x1
#            print "x text %s"%tostring(text, textsize)  
#            print "x val %d, pos %d -> shift: %d\n"%(val, pos, (textsize - ((pos-1)+1)))  
            binlst = DES._append(binlst, val)
        return binlst

    @staticmethod
    def _string2hex(text):
        return int(text.encode('hex'),16)

    @staticmethod
    def _hex2string(hexadecimal):
        text = "%x"%hexadecimal
        return ''.join(chr(int(text[i:i+2], 16)) for i in range(0, len(text), 2))

    def encrypt(self, plaintext, ishex=False):
        ## params
        ## plaintext = the plaintext as string or as hex number
        ## ishex = if the plaintext was a hex number (True)
        
#        if len(plaintext) == 0: die("ERROR plaintext was empty")    
        

        ## init
        if ishex: state = plaintext
#        else: state = int(plaintext.encode('hex'),16) & 0xffffffffffffffff  
        else: state = DES._string2hex(plaintext) & 0xffffffffffffffff
        DBG( "\n\nENCRYPTION\n\nplaintext:         %#s"%tostring(state, 64) )

        ## 1. initial permutation
        ## Note that both permutations do not increase the security of DES at all
        ## takes 64-bit input, result is
        state = DES._map_by_table(state, self._ip._initial_permutation, 64)
        DBG("1. initial permutation")
        DBG("\tstate      %s"%tostring(state, 64))

        ## F-function
        for idx in range(16):
            ## DES loops the following steps
            ## 2. split
            left_half, right_half = self._ffunc.split(state)
            DBG("2. split")
            DBG("\tstate      %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

            ## 3. expansion permutation
            right_exp = self._ffunc.expansion(right_half)
            DBG("3. expansion permutation")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 48)))

            ## 4. apply key
            right_exp = self._ffunc.encryptkey(right_exp,idx)
            DBG("4. apply key")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 48)))

            ## 5. s-boxes
            right_exp = self._ffunc.sbox(right_exp)
            DBG("5. s-box substitution")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 32)))

            ## 6. permutation
            ## finally, the 32-bit output is permuted bitwise according to the
            ## P permutation; unlike the initial IP and its inverse IP-1, the
            ## permutation P introduces diffusion because the four output bits of
            ## each S-box are permuted in such a way that they affect several
            ## different S-boxes in the following round
            ## takes a 32-bit input, result is 32-bit
            right_exp = self._map_by_table(right_exp, self._ffunc._pbox, 32)
            DBG("6. permutation")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 32)))

            ## 7. xor left and right half
            left_half ^= right_exp
            DBG("7. xor left and right half key")
            DBG("\tstate      %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

            ## 8. merge and switch halves
            state = DES._append(right_half, left_half, 32)
            DBG("8. merge and switch halves")
            DBG("\tstate      %s"%tostring(state, 64))
            DBG("")

        ## DES loops the following steps
        ## final split
        left_half, right_half = self._ffunc.split(state)
        DBG("final split")
        DBG("\tstate      %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

        ## final merge and switch halves
        state = DES._append(right_half, left_half, 32)
        DBG("final merge and switch halves")
        DBG("\tstate      %s"%tostring(state, 64))

        ## revert permutation
        ## Note that both permutations do not increase the security of DES at all
        state = DES._map_by_table(state, self._ip._final_permutation, 64)
        DBG("9. final permutation")
        DBG("\tstate      %s"%tostring(state, 64))
        return state

    def decrypt(self, ciphertext):
        DBG( "\n\nDECRYPTION\n\nplaintext:         %#s"%tostring(ciphertext, 64) )

        ## 1. initial permutation
        ## Note that both permutations do not increase the security of DES at all
        ## takes 64-bit input, result is
        state = DES._map_by_table(ciphertext, self._ip._initial_permutation, 64)
        DBG("1. initial permutation")
        DBG("\tstate      %s"%(tostring(state, 64)))

        ## F-function
        for idx in range(16):
            ## DES loops the following steps
            ## 2. split
            ## in decryption, left and right halves are twisted!!!
#            right_half, left_half = self._ffunc.split(state)
            left_half, right_half = self._ffunc.split(state)
            DBG("2. split")
            DBG("\tstate      %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

            ## 3. expansion permutation
            right_exp = self._ffunc.expansion(right_half)
            DBG("3. expansion permutation")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 48)))

            ## 4. key
            right_exp = self._ffunc.decryptkey(right_exp,idx)
            DBG("4. key")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 48)))

            ## 5. s-boxes
            right_exp = self._ffunc.sbox(right_exp)
            DBG("5. s-box substitution")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 32)))

            ## 6. permutation
            ## finally, the 32-bit output is permuted bitwise according to the
            ## P permutation; unlike the initial IP and its inverse IP-1, the
            ## permutation P introduces diffusion because the four output bits of
            ## each S-box are permuted in such a way that they affect several
            ## different S-boxes in the following round
            ## takes a 32-bit input, result is 32-bit
            right_exp = self._map_by_table(right_exp, self._ffunc._pbox, 32)
            DBG("6. permutation")
            DBG("\tstate      %s %s | %s"%(tostring(left_half, 32), tostring(right_half, 32), tostring(right_exp, 32)))

            ## 7. xor left and right half
            left_half ^= right_exp
            DBG("7. xor left and right half")
            DBG("\tstate      %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

            ## 8. switch halves
            ## in decryption, left and right halves are twisted!!!
            state = DES._append(right_half, left_half, 32)
            DBG("8. merge and switch halves")
            DBG("\tstate      %s"%tostring(state, 64))
            DBG("")

            
        ## DES loops the following steps
        ## final split
        left_half, right_half = self._ffunc.split(state)
        DBG("final split")
        DBG("\tstate      %s %s"%(tostring(left_half, 32), tostring(right_half, 32)))

        ## final merge and switch halves
        state = DES._append(right_half, left_half, 32)
        DBG("final merge and switch halves")
        DBG("\tstate      %s"%tostring(state, 64))

        ## 9. revert permutation
        ## Note that both permutations do not increase the security of DES at all
        state = DES._map_by_table(state, self._ip._final_permutation, 64)
        DBG("9. final permutation")
        DBG("\tstate      %s"%tostring(state, 64))

        
        print "\n\nfinal:\n%s"%tostring(state, 64)  
        die("STOP")
        

        ## convert to string
        return DES._hex2string(state)


### main ###
def main(argv=sys.argv[1:]):
    blocksize = 64 # TODO use   
    keysize_with_parity = 64
    inputkey = 0xffffffffffffffff   
    plaintext = ""
# TODO use  
    keylength = 64

    if len(argv) > 0:
        ## offer encryption by command line argument
        try:
            inputkey = int(argv[0],16)
            plaintext = argv[1]
        except:
            die('usage: either w/o arguments, or as follows\n$ %s <inputkey> "<plaintext>"\ne.g.\n$ %s %s "%s"'%(sys.argv[0],sys.argv[0],"0x000102030405060708090a0b0c0d0e0f","from Disco to Disco.."))
    else:
        ## init some raw input key example
        inputkey = 0x0001020304050607 #08090a0b0c0d0e0f
        ## init some input text example
        plaintext = "jack and jill went up the hill to fetch a pail of water"
    
# TODO rm
#    inputkey = 0xffffffffffffffff   
#    inputkey =  0x0000000000000080  

#        plaintext = "Angelina"      
        
#        inputkey =  0x0000000000000002  
#        plaintext = 0x8000000000000000  

#        plaintext = "A" # TODO, strings inferior to blocksize  

        inputkey = 0x5B5A57676A56676E
        plaintext = 0x675A69675E5A6B5A


    

    print "initial key:\n%#.32x, key length %d, block size %d\n" % (inputkey, keylength, blocksize)

    print "plaintext:"
    print "%s\n" % plaintext

    ## init the algorithm
    des = DES(inputkey)

#    print "XXX %s"%tostring( des.encrypt(plaintext,ishex=True), 64)    
    ciphertext = []
    ciphertext.append(des.encrypt(plaintext,ishex=True))
#    die("STOP")   

    ## some input text
    ## blocks
# TODO uncomment                

###    
#    idx = 0  
## FIXME: is idx globally defined in other codes?
#    ciphertext = []
#    blocktext = ""
#    for idx in range(len(plaintext)-1):
#        blocktext += plaintext[idx]
#        if idx % (blocksize/8) == 0:
#            ciphertext.append(des.encrypt(blocktext))
#            blocktext = ""
#            
#    blocktext += plaintext[idx+1] # TODO what if there is only block 0?
#    
#    ciphertext.append(des.encrypt(blocktext))

    ## print result
    print "encrypted:"
    for item in ciphertext:
        print "%s"%tostring(item, 64)
    print "\n"

    ## decrypt
    decryptedtext = ""
    for block in ciphertext:
        decryptedtext += des.decrypt(block)

    ## print result
# FIXME
    print "decrypted:"
    print "%s\n" % decryptedtext


### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
