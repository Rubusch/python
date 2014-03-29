#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
@author: Lothar Rubusch
@email: L.Rubusch@gmx.ch
@license: GPLv3
@2014-Mar-19

AES (american encryption standard)
128-bit block size
key lengths of 128 bit, 192 bit or 256 bit


AES example

Key:        000102030405060708090a0b0c0d0e0f
Plaintext:  00112233445566778899aabbccddeeff
Ciphertext: 69c4e0d86a7b0430d8cdb78070b4c55a
"""

import sys

### utils ###
def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)

def DBG(msg):
    print msg
    pass

class AES:
    def __init__(self, inputkey, keylength):
        ## blocksize
        self._blocksize = 128

        ## S-box
        self._sbox = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
                      [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
                      [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
                      [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
                      [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
                      [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
                      [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
                      [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
                      [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
                      [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
                      [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
                      [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
                      [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
                      [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
                      [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
                      [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

        self._inv_sbox = self._invert_sbox(self._sbox)

        ## diffusion layer
        self._shift_rows = [0,5,10,15,4,9,14,3,8,13,2,7,12,1,6,11]
        self._inv_shift_rows = [self._shift_rows.index(idx) for idx in range(len(self._shift_rows))]

        self._mix_columns__const_matrix = [[2,3,1,1],
                                           [1,2,3,1],
                                           [1,1,2,3],
                                           [3,1,1,2]]
# TODO invert _mix_columns__const_matrix  
# TODO use 4-byte groups instead of one single line

        ## Rcon, source: http://en.wikipedia.org/wiki/Rijndael_key_schedule
        ## only the first some are actually used!!!
        self._rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

        ## key schedule
        self._keylength = keylength
        self._rounds = 10
        if 192 == self._keylength: self._rounds = 12
        elif 256 == self._keylength: self._rounds = 14
        self._keys = self._key_schedule(inputkey, self._keylength)

    def _key_schedule(self, password, keylength):
        ## init, e.g. keylength 128 and password:
        ## 0x000102030405060708090a0b0c0d0e0f
        Nb = 4
        Nk = keylength / 32
        Nr = Nk + 6 # rounds keys
        words = []
        words = [0] * Nb * (Nr+1)
        temp = 0x0

        ## split initial key into four pieces
        ## 0x00010203 0x04050607 0x08090a0b 0x0c0d0e0f
        for idx in range(Nk):
            words[idx] = (password >>(keylength - (idx+1) * 32)) & 0xffffffff

        for idx in range(Nk, Nb*(Nr+1)): # round 4. -> 44. (128-bit)
            words[idx] = 0x0

            ## init temp to the last quadruple
            temp = words[idx-1]

            nextword = 0x0
            if idx % Nk == 0:
                ## first word block, rotate and substitute

                ## rotate word
                swap = (temp >>24) & 0xff
                temp = ((temp <<8) & 0xffffffff)|swap
                ## temp: 0x0d0e0f0c

                ## s-boxing and r-coefficient
                for sub in range(4):
                    ## s-boxing
                    row = (temp >> (32 - 8*(sub+1) + 4)) & 0xf
                    col = (temp >> (32 - 8*(sub+1))) & 0xf
                    ch = self._sbox[row][col]
                    ## ch: d7

                    ## the 0. char, XOR against round coefficient
                    if sub == 0: ch ^= self._rcon[idx/Nk -1]
                    ## ch: d7

                    ## append new character
                    nextword = (nextword<<8) | ch
                    ## swap: d6

                temp = nextword
                ## temp: 0xd6ab76fe

            elif Nk > 6 and idx % Nk == 4:
                ## keylength above 128-bit, additional substitutions
                for sub in range(4):
                    ## s-boxing
                    row = (temp >> (32 - 8*(sub+1) + 4)) & 0xf
                    col = (temp >> (32 - 8*(sub+1))) & 0xf
                    ch = self._sbox[row][col]

                    ## append new character
                    nextword = (nextword<<8) | ch

                temp = nextword
                ## temp: 0xd6ab76fe

            ## assign the preceeding word, XORed against the current temp
            words[idx] = words[idx-Nk] ^ temp
        return words

    ## utilities
    def _invert_sbox(self, box):
        box_inv = []
        for val in range(len(box)*len(box[0])):
            row = 0
            col = 0
            for row in range(len(box)):
                try:
                    col = box[row].index(val)
                    break
                except ValueError:
                    next
            ## invert row, col and value
            val_inv = row
            val_inv = (val_inv<<4)|col
            row_inv = val&0xf
            col_inv = (val<<4)&0xf
            if 0 == col_inv: box_inv.append([])
            box_inv[row_inv].append(val_inv)
        return box_inv

# TODO replace
    def _hexlst_getnth(self, hexlst, nth, size):
        ## return the nth 8-bit number, contained in the hex list (a number)
        ## where nth is an index, starting with 0
        return ((hexlst >> (size - (nth+1)*8)) & 0xff)

# TODO replace
    def _hexlst_append(self, hexlst, val, nbytes=1):
        ## appends an 8-bit hex val to a hex list (a number) of such values
        ## and returns it
        return ((hexlst << (8*nbytes))|val)

    def _lst_XOR(self, lst):
        ## XORs all lists entries in a list, and returns a result in GF(2^8), so
        ## an 8-bit value
        ret = 0x0
        for item in lst:
            ret ^= item
        return (ret&0xff)

    def _add_round_key(self, state, rnd):
        ## add a round key
        key = self._keys[rnd*4]
        key = key <<32 | self._keys[rnd*4+1]
        key = key <<32 | self._keys[rnd*4+2]
        key = key <<32 | self._keys[rnd*4+3]
        ret = key ^ state
        DBG( "R%d (key = %#.32x)\t= %#.32x" % (rnd,key,ret) )
        return ret

    def _substitution_layer__sub_bytes(self, state):
        ## substitution per 8-bit values
        hexlst = 0x0
        for idx in range(self._blocksize/8):
            ch = (state >> (self._blocksize - (idx+1)*8)) & 0xff
            row = 0xf & (ch >>4)
            col = 0xf & ch
            val = self._sbox[row][col]
            hexlst = self._hexlst_append(hexlst, val)
        return hexlst

    def _diffusion_layer__shift_rows(self, state):
        ## first operation in the diffusion layer on 8-bit values
        hexlst = 0x0
        for idx in range(self._blocksize/8):
            hexlst = self._hexlst_append(hexlst, self._hexlst_getnth(state, self._shift_rows[idx], self._blocksize))
        return hexlst

    def _diffusion_layer__mix_column(self, state):
        ## major diffusion element on 8-bit values
        ##
        ## matrix-matrix-multiplication in GF(2^8) with P(x) = x^8 + x^4 + x^3 + x + 1
        ##
        ##  / c0 \      / 2 3 1 1 \     / b0 \
        ## |  c1  |    |  1 2 3 1  |   |  b1  |
        ## |  c2  | == |  1 1 2 3  | * |  b2  |
        ##  \ c3 /      \ 3 1 1 2 /     \ b3 /
        ##
        ## where B = state/input, and C = states/output
        ##
        ## Galois Field restrictions:
        ## * Addition: XOR operation
        ## * Multiplication: leftshift, with modular reduction to P(x)
        ##
        ## in specific:
        ## * the factor 1 will multiply by identity, means just take the b-value
        ## * the factor 2 is a doubling (leftshift by 1) and modular reduction
        ##   here named b vector
        ## * the factor 3 is a XOR combination of 1 and 2, since 3x = x + 2x,
        ##   here named bb and b vector
        hexlst = 0x0
        for col in range(len(self._mix_columns__const_matrix[0])):
            b_vec = [0]*4
            bb_vec = [0]*4
            for row in range(len(self._mix_columns__const_matrix)):
                ## 1. left shift by factor for each vector value
                ## 2. XOR the shifted vector results
                b_vec[row] = self._hexlst_getnth(state, row+(4*col), self._blocksize)

                ## write doubled b-values into bb-vec,
                ## GF(2^8), perform modular reduction by mod P(x), which is
                ## P(x) = x^8 + x^4 + x^3 + x + 1
                ## if b_vec[row] & 0x80:
                ##     bb_vec[row] = b_vec[row] <<1 ^ 0x11b
                ## else:
                ##     bb_vec[row] = b_vec[row] <<1
                ## brief writing of the above
                bb_vec[row] = b_vec[row] <<1 ^ 0x11b if b_vec[row] & 0x80 else b_vec[row] <<1

            hexlst = self._hexlst_append(hexlst, (bb_vec[0] ^  b_vec[1] ^ bb_vec[1] ^  b_vec[2] ^  b_vec[3]))
            hexlst = self._hexlst_append(hexlst, ( b_vec[0] ^ bb_vec[1] ^  b_vec[2] ^ bb_vec[2] ^  b_vec[3]))
            hexlst = self._hexlst_append(hexlst, ( b_vec[0] ^  b_vec[1] ^ bb_vec[2] ^  b_vec[3] ^ bb_vec[3]))
            hexlst = self._hexlst_append(hexlst, ( b_vec[0] ^ bb_vec[0] ^  b_vec[1] ^  b_vec[2] ^ bb_vec[3]))
        return hexlst




    
    def _substitution_layer__inv_sub_bytes(self, state):
        ## substitution per 8-bit values
        hexlst = 0x0
        for idx in range(self._blocksize/8):
            ch = (state >> (self._blocksize - (idx+1)*8)) & 0xff
            row = 0xf & (ch >>4)
            col = 0xf & ch
            val = self._inv_sbox[row][col]
            hexlst = self._hexlst_append(hexlst, val) 
        return hexlst

    def _diffusion_layer__inv_shift_rows(self, state):
        ## first operation in the diffusion layer on 8-bit values
        hexlst = 0x0
        for idx in range(self._blocksize/8):
#            hexlst = self._hexlst_append(hexlst, self._hexlst_getnth(state, self._shift_rows[idx], self._blocksize))
            hexlst = self._hexlst_append(hexlst, self._hexlst_getnth(state, self._inv_shift_rows[idx], self._blocksize))  
        return hexlst

    def _diffusion_layer__inv_mix_column(self, state):
        return state
        
#        ## major diffusion element on 8-bit values
#        ##
#        ## matrix-matrix-multiplication in GF(2^8) with P(x) = x^8 + x^4 + x^3 + x + 1
#        ##
#        ##  / c0 \      / 2 3 1 1 \     / b0 \
#        ## |  c1  |    |  1 2 3 1  |   |  b1  |
#        ## |  c2  | == |  1 1 2 3  | * |  b2  |
#        ##  \ c3 /      \ 3 1 1 2 /     \ b3 /
#        ##
#        ## where B = state/input, and C = states/output
#        ##
#        ## Galois Field restrictions:
#        ## * Addition: XOR operation
#        ## * Multiplication: leftshift, with modular reduction to P(x)
#        ##
#        ## in specific:
#        ## * the factor 1 will multiply by identity, means just take the b-value
#        ## * the factor 2 is a doubling (leftshift by 1) and modular reduction
#        ##   here named b vector
#        ## * the factor 3 is a XOR combination of 1 and 2, since 3x = x + 2x,
#        ##   here named bb and b vector
#        hexlst = 0x0
#        for col in range(len(self._mix_columns__const_matrix[0])):
#            b_vec = [0]*4
#            bb_vec = [0]*4
#            for row in range(len(self._mix_columns__const_matrix)):
#                ## 1. left shift by factor for each vector value
#                ## 2. XOR the shifted vector results
#                b_vec[row] = self._hexlst_getnth(state, row+(4*col), self._blocksize)
#
#                ## write doubled b-values into bb-vec,
#                ## GF(2^8), perform modular reduction by mod P(x), which is
#                ## P(x) = x^8 + x^4 + x^3 + x + 1
#                ## if b_vec[row] & 0x80:
#                ##     bb_vec[row] = b_vec[row] <<1 ^ 0x11b
#                ## else:
#                ##     bb_vec[row] = b_vec[row] <<1
#                ## brief writing of the above
#                bb_vec[row] = b_vec[row] <<1 ^ 0x11b if b_vec[row] & 0x80 else b_vec[row] <<1
#
#            hexlst = self._hexlst_append(hexlst, (bb_vec[0] ^  b_vec[1] ^ bb_vec[1] ^  b_vec[2] ^  b_vec[3]))
#            hexlst = self._hexlst_append(hexlst, ( b_vec[0] ^ bb_vec[1] ^  b_vec[2] ^ bb_vec[2] ^  b_vec[3]))
#            hexlst = self._hexlst_append(hexlst, ( b_vec[0] ^  b_vec[1] ^ bb_vec[2] ^  b_vec[3] ^ bb_vec[3]))
#            hexlst = self._hexlst_append(hexlst, ( b_vec[0] ^ bb_vec[0] ^  b_vec[1] ^  b_vec[2] ^ bb_vec[3]))
#        return hexlst
    

    def encrypt(self, plaintext):
        ## init
        state = int(plaintext.encode('hex'),16) & 0xffffffffffffffffffffffffffffffff

        
        ## DEBUG
        state = 0xffffffffffffffffffffffffffffffff 
        state = 0x00112233445566778899aabbccddeeff
#        state = 0x00000000000000000000000000000000
        

        ## round 0
        state = self._add_round_key(state, 0)
        DBG( "add key: \t%#.32x"%state )

        for rnd in range(self._rounds-1):
            DBG( "rnd %d"%rnd )

            state = self._substitution_layer__sub_bytes(state)
            DBG( "substitute: \t\t%#.32x"%state )

            state = self._diffusion_layer__shift_rows(state)
            DBG( "shift rows: \t\t%#.32x"%state )

            state = self._diffusion_layer__mix_column(state)
            DBG( "mix column: \t\t%#.32x"%state )

            state = self._add_round_key(state, rnd+1)
            DBG( "add key: \t\t%#.32x"%state )
            DBG("")

        ## round n
        state = self._substitution_layer__sub_bytes(state)
        DBG( "substitute: \t%#.32x"%state )

        state = self._diffusion_layer__shift_rows(state)
        DBG( "shift rows: \t%#.32x"%state )

        state = self._add_round_key(state, self._rounds)
        DBG( "add key: \t%#.32x"%state )

        return state


    def decrypt(self, ciphertext):

        state = ciphertext  
#        state = 0x00112233445566778899aabbccddeeff

        ## round n
        state = self._add_round_key(state, self._rounds)
        DBG( "add key: \t%#.32x"%state )

        state = self._diffusion_layer__inv_shift_rows(state)
        DBG( "shift rows: \t%#.32x"%state )

        state = self._substitution_layer__inv_sub_bytes(state)
        DBG( "substitute: \t%#.32x"%state )

        for rnd in range(self._rounds-1,0,-1):
            DBG( "rnd %d"%rnd )

            state = self._add_round_key(state, rnd+1)
            DBG( "add key: \t\t%#.32x"%state )

            state = self._diffusion_layer__inv_mix_column(state)
            DBG( "mix column: \t\t%#.32x"%state )

            state = self._diffusion_layer__inv_shift_rows(state)
            DBG( "shift rows: \t\t%#.32x"%state )

            state = self._substitution_layer__inv_sub_bytes(state)
            DBG( "substitute: \t\t%#.32x"%state )
            DBG("")

        ## round 0
        state = self._add_round_key(state, 0)
        DBG( "add key: \t%#.32x"%state )


        die("STOP")    
        return state


### main ###
def main():
    blocksize = 128

    ## init some raw input key
    inputkey = 0x000102030405060708090a0b0c0d0e0f

    print "initial key:\n%#.32x\n" % inputkey

    ## init the algorithm
    aes = AES(inputkey, 128)

    ## init some input text
    plaintext = "jack and jill went up the hill to fetch a pail of water"
#    print "plaintext:"
#    print "%s\n" % plaintext

    ciphertext = []
    blocktext = ""
# TODO handle blocks..
    # for idx in range(len(plaintext)-1):
    #     blocktext += plaintext[idx]
    #     if idx % (blocksize/8) == 0:
    #         ciphertext.append(aes.encrypt(blocktext))
    #         blocktext = ""
    # blocktext += plaintext[idx+1]
    # ciphertext.append(aes.encrypt(blocktext))

    blocktext += plaintext[0]
    ciphertext.append(aes.encrypt(blocktext))

    ## print result
    print "encrypted:"
    for item in ciphertext:
        print "%#.32x"%item
    print "\n"

    ## decrypt
    decryptedtext = ""
    for block in ciphertext:
        decryptedtext += aes.decrypt(block)

    ## print result
    print "decrypted:"
    print "%s\n" % decryptedtext

### start ###
if __name__ == '__main__':
    main()
print "READY.\n"
