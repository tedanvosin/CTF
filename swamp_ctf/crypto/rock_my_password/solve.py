from pwn import *

from Crypto.Hash import SHA256, SHA512, MD5

f= open("rockyou.txt", "rb")

while True:
    password = f.readline().strip()
    
    if len(password) != 10:
        continue
    
    flag = b'swampCTF{'+ password + b'}'
    for i in range(100):
        flag = MD5.new(flag).digest()
        # print(flag)

    for i in range(100):
        flag = SHA256.new(flag).digest()
        # print(flag)
    
    for i in range(100):
        flag = SHA512.new(flag).digest()
        # print(flag)

    print(flag.hex())
    if flag.hex() == "f600d59a5cdd245a45297079299f2fcd811a8c5461d979f09b73d21b11fbb4f899389e588745c6a9af13749eebbdc2e72336cc57ccf90953e6f9096996a58dcc":
        print("Found the password:", password.decode())
        break

    #password=secretcode