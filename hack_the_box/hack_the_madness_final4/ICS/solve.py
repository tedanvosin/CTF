from pwn import *
import json
import pprint
pr = remote('94.237.63.165',41784)

pr.recvuntil(b'>> ')
pr.sendline(b'1')
ln = json.loads(pr.recvline().strip().decode().replace("\'","\""))
pprint.pprint(ln)

pr.interactive()