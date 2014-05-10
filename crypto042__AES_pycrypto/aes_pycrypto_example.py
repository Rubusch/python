#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# @author: Lothar Rubusch
# @email: L.Rubusch@gmx.ch
# @license: GPLv3
# @2014-Mar-19
#
# based on http://www.commx.ws/2013/10/aes-encryption-with-python/
# framework example
#
#!/usr/bin/env python2.7

from Crypto import Random
from Crypto.Cipher import AES

def encrypt(plaintext, key=None, key_size=256):
    def pad(s):
        x = AES.block_size - len(s) % AES.block_size
        return s + (chr(x) * x)

    padded_plaintext = pad(plaintext)

    if key is None:
        key = Random.OSRNG.posix.new().read(key_size // 8)

    iv = Random.OSRNG.posix.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return (iv + cipher.encrypt(padded_plaintext), key)

def decrypt(ciphertext, key):
    unpad = lambda s: s[:-ord(s[-1])]
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))[AES.block_size:]

    return plaintext

if __name__ == '__main__':
    ## a random key will be taken and returned together with the ciphered text
    ## the pair "randomkey + ciphered text" then will be passed to the decrypt
    ## function (that's why the ciphered printout looks always different);
    ## in addition an IV will be applied at encryption (CBC ?)
    plaintext = b"Horum omnium fortissimi sunt Belgae, propterea quod a cultu "\
        "atque humanitate provinciae longissime absunt, minimeque ad eos " \
        "mercatores saepe commeant atque ea quae ad effeminandos animos " \
        "pertinent important, proximique sunt Germanis, qui trans Rhenum " \
        "incolunt, quibuscum continenter bellum gerunt."
    print "plaintext:\n%s\n" % plaintext

    ciphertext_and_key = encrypt(plaintext)
    print "encrypted:\n%s\n" % "".join(map(str,ciphertext_and_key[0]))

    decryptedtext = decrypt(*ciphertext_and_key) ## pass ciphertext and key
    print "decrypted:\n%s\n" % decryptedtext

    assert decryptedtext == plaintext
