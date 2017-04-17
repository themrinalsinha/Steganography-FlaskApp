from Crypto import Random
from Crypto.Cipher import AES
# from xterminate_stegano import *
import base64

import binascii

BLOCK_SIZE = 16

def encrypt(message, passphrase):
    IV = Random.new().read(BLOCK_SIZE)
    aes = AES.new(passphrase, AES.MODE_CFB, IV)
    return base64.b64encode(IV + aes.encrypt(message))

def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    IV = encrypted[:BLOCK_SIZE]
    aes = AES.new(passphrase, AES.MODE_CFB, IV)
    return aes.decrypt(encrypted[BLOCK_SIZE:])

if __name__ == "__main__":
    main()



# def xterm_enc(key, message):
#
#     if len(message) % 16 != 0:
#         message += ' ' * (16 - len(message) % 16)
#
#     encryption_suite = AES.new(key, AES.MODE_CBC, iv)
#     cipher_text = encryption_suite.encrypt(message)
#     return cipher_text
#
# def xterm_dec(key, cipher_message):
#     decryption_suite = AES.new(key, AES.MODE_CBC, iv)
#     return(decryption_suite.decrypt(cipher_message))
#
# if __name__ == '__main__':
#     main()


# Encryption
# encryption_suite = AES.new('This is a key123', AES.MODE_CBC, Random.new().read(AES.block_size))
# cipher_text = encryption_suite.encrypt("A really secret message. Not for prying eyes.")

# Decryption
# decryption_suite = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# plain_text = decryption_suite.decrypt(cipher_text)
# cipher_text = xterm_enc("89fff5fa871a4af5944e4e56b75bd114", "Hello World, This is me just testing if it really works...")
# print(cipher_text)
# print(xterm_dec("89fff5fa871a4af5944e4e56b75bd114", cipher_text))
