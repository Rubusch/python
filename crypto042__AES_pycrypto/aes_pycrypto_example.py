#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-19
#
# (c) Original from http://www.commx.ws/2013/10/aes-encryption-with-python/
# framework example
#
#!/usr/bin/env python2.7

from Crypto import Random
from Crypto.Cipher import AES

def encrypt(message, key=None, key_size=256):
    def pad(s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (chr(x) * x)

    padded_message = pad(message)

    if key is None:
        key = Random.OSRNG.posix.new().read(key_size // 8)

    iv = Random.OSRNG.posix.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return (iv + cipher.encrypt(padded_message), key)

def decrypt(ciphertext, key):
    unpad = lambda s: s[:-ord(s[-1])]
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))[AES.block_size:]

    return plaintext

if __name__ == '__main__':
    message = b"jack and jill went up the hill to fetch a pail of water"
    print "message: \t%s" % message

    encrypted = encrypt(message)
    print "encrypted: \t%s" % "".join(map(str,encrypted))

    decrypted = decrypt(*encrypted)
    print "decrypted: \t%s" % decrypted

    assert decrypted == message
