from pwn import *

k=b''
for i in range(0x10000):
    k+=p32(i)

with open('gadgets', 'wb') as f:
    f.write(k)