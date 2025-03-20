from AES import encrypt, pad, unpad, decrypt
import json
import os
from pwn import *

def func():
    pr = process(['python', 'server.py'])
    ln = pr.recvline()
    ln = json.loads(ln)
    key = bytes.fromhex(ln['key'])
    ciphertext = bytes.fromhex(ln['ciphertext'])
    my_iv=os.urandom(16)
    print(decrypt(key, ciphertext,mode="CBC",iv=my_iv))
    return


    for _ in range(10):
        iv = os.urandom(8)*2
        key = os.urandom(16) 
        try:
            ciphertext = encrypt(key, plaintext, mode="CBC", iv=iv)
        except:
            EXIT()
        print(json.dumps({
            'key': key.hex(),
            'ciphertext': ciphertext.hex()
        }))
        inp = input("Enter iv: ")
        if (iv.hex() != inp):
            EXIT()
        print()

    plaintext = pad(secret, 16)
    iv = os.urandom(8)*2
    key = os.urandom(16)
    try:
        ciphertext = encrypt(key, plaintext, mode="CBC", iv=iv) 
    except:
        EXIT()
    print(json.dumps({
        'key': key.hex(),
        'ciphertext': ciphertext.hex()
    }))

func()