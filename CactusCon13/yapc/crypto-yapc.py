from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

FLAG = b'flag{fake-flag-for-testing}'
key = os.urandom(16)
cipher = AES.new(key=key, mode=AES.MODE_ECB)

print("""
      Welcome to yet another padding challenge

      mmmmmm   mmm  mmmmm    m      m      m
      #      m"   " #    #   #      #      #
      #mmmmm #      #mmmm"   #      #      #
      #      #      #    #   "      "      "
      #mmmmm  "mmm" #mmmm"   #      #      #
      """)
while True:
    try:
        plaintext_prefix = input("Input: ").encode()
    except:
        break
    ciphertext = cipher.encrypt(pad(plaintext_prefix + FLAG, cipher.block_size))
    print("Cipher:", ciphertext.hex())
