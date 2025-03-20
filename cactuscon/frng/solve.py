from pwn import *
import json
import random
import hashlib
from Crypto.Util.number import bytes_to_long, inverse
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
from randcrack import RandCrack

pr = remote('104.131.177.253', 31092)
rc = RandCrack()
#print(pr.recvall(timeout=1))
for i in range(624):
    pr.recvuntil(b'Enter your option: ')

    pr.sendline(b'3')
    pr.recvuntil(b'cheer you up:')
    rand_num = int(pr.recvline().strip(),10)
    rc.submit(rand_num)
    print(f'number {i} processed')

pr.recvuntil(b'Enter your option: ')
pr.sendline(b'1')

ln = pr.recvline().strip().decode().replace('\'','\"')
recv_json = json.loads(ln)
r = int(recv_json["r"],16)
s = int(recv_json["s"],16)
msg = recv_json["msg"]
k = rc.predict_getrandbits(192)

order = generator_192.order()

# Compute the message hash
h = bytes_to_long(hashlib.sha1(msg.encode()).digest())

# Recover private key using the formula x = (s * k - h) / r mod order
d = ((s * k - h) * inverse(r, order)) % order


#print(f"Recovered Private Key: {hex(d)}")

forge_msg = "open seasame"
h_forge = bytes_to_long(hashlib.sha1(forge_msg.encode()).digest())

pubkey = Public_key(generator_192, generator_192 * d)
privkey = Private_key(pubkey, d)

sig_forge = privkey.sign(h_forge, k)

payload = json.dumps({"msg": forge_msg, "r": hex(sig_forge.r), "s": hex(sig_forge.s)})

pr.recvuntil(b'Enter your option: ')
pr.sendline(b'2')
pr.recvuntil(b'format: ')
pr.sendline(payload.encode())
print(pr.recvall(timeout=1).decode())