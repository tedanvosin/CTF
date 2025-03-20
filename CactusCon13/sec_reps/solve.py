from pwn import *
from hashlib import md5
import string

pr = remote('138.197.116.162' ,32649)

flag = b''


while len(flag)==0 or flag[-1]!=b'}':

    base_hex = md5(b'\x00'*(len(flag)+1)).hexdigest()
    print(base_hex)
    for c in string.printable:
        #print(f'Trying c = {c}')
        pr.recvuntil(b'> ')
        pr.sendline(b'1')
        pr.recvuntil(b'Enter your message: ')
        pr.sendline(flag+c.encode())
        pr.recvuntil(b'Hash: ')
        recv_hash = pr.recvline().strip().decode()
        if recv_hash == base_hex:
            flag+=c.encode()
            print(f'Found a flag character:{flag.decode()}')
            break

