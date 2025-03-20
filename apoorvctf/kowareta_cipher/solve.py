from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

#pr = process(['python', 'Chall.py'])
pr= remote('chals1.apoorvctf.xyz',4001)

flag = b''

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

for i in range(32):
    pr.recvuntil(b'Enter your input: ')
    payload = b'A'*(i+1)
    #print(payload.hex())
    pr.sendline(payload.hex().encode())
    pr.recvuntil(b'Ciphertext: ')
    enc = pr.recvline().strip()
    enc = bytes.fromhex(enc.decode())
    enc = divide_chunks(enc, 16)
    enc = list(enc)
    
    for c in string.printable:
        c = c.encode()
        pr.recvuntil(b'Enter your input: ')
        payload = c+flag+b'A'*(i+1)
        payload = pad(payload,16)
        pr.sendline(payload.hex().encode())
        pr.recvuntil(b'Ciphertext: ')
        enc_ch = pr.recvline().strip()
        enc_ch = bytes.fromhex(enc_ch.decode())
        enc_ch = divide_chunks(enc_ch, 16)
        enc_ch = list(enc_ch)
        if enc_ch[0] == enc[2]:
            flag = c+flag
            print(flag)
            break