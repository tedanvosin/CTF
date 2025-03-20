from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad

pr = remote()

buff = b'a'*5
for i in range(43):
    pr.recvuntil(b'')
    pr.send(b'\x00')
