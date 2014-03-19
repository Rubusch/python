#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-19
#
# AES (american encryption standard)
# 128-bit block size
# key lengths of 128 bit, 192 bit or 256 bit

import sys

### utils ###
def die(msg):
    if 0 < len(msg): print msg
    sys.exit(1)


class AES:
    def __init__(self, inputkey):
        
        pass

    def encrypt(self, plaintext):
        pass

    def decrypt(self, ciphertext):
        pass


### main ###
def main():
    blocksize = 128

    ## init some raw input key
    inputkey = 0xffffffffffffffff
    print "initial key:"
    print "%#x\n" % inputkey

    ## init the algorithm
    aes = AES(inputkey)

    ## init some input text
    plaintext = "jack and jill went up the hill to fetch a pail of water"
    print "plaintext:"
    print "%s\n" % plaintext

    ciphertext = []
    blocktext = ""
    for idx in range(len(plaintext)-1):
        blocktext += plaintext[idx]
        if idx % (blocksize/8) == 0:
            ciphertext.append(aes.encrypt(blocktext))
            blocktext = ""
    blocktext += plaintext[idx+1]
    ciphertext.append(aes.encrypt(blocktext))

    ## print result
    print "encrypted:"
    for item in ciphertext:
        print "%#x"%item,
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
