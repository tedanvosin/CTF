from pwn import *
from randcrack import RandCrack
from hashlib import sha256
from Crypto.Util.number import isPrime
from random import randbytes


rc = RandCrack()
# pr = process('./server.py')
pr = remote('leet-prime.atreides.b01lersc.tf', 8443,ssl=True)

def solve_pow(prefix: bytes) -> bytes:
    for i in range(2**32):
        suffix = randbytes(6)
        h = sha256(prefix + suffix).digest()
        if int.from_bytes(h, 'big') >> (256 - 24) == 0:
            return suffix
    
    raise RuntimeError("PoW solution not found.")

for i in range(624):
    pr.recvuntil(b': ')
    ln = bytes.fromhex(pr.recvline().strip().decode())
    ln = int.from_bytes(ln, 'little')
    # print(ln)
    rc.submit(ln)
    pr.recvuntil(b'ans (hex): ')
    pr.sendline(b'0'*64)

# solve_proof_of_work
pr.recvuntil(b': ')
ln = bytes.fromhex(pr.recvline().strip().decode())
rc.predict_getrandbits(32)

print(b'Start Solving Proof of Work')
suff = solve_pow(ln)

pr.recvuntil(b'ans (hex): ')
pr.sendline(suff.hex().encode())

f = lambda nbits: rc.predict_randint(13, 37).to_bytes(nbits, 'big')

# print(rc.predict_getrandbits(24))
while True:
    pred = rc.predict_getrandbits(24)
    # print(pred)
    leet_prime = int.from_bytes(pred.to_bytes(3,'little'), 'big')
    if isPrime(leet_prime, false_positive_prob=133e-7, randfunc=f):
        break

for i in range(1337):
    pr.recvuntil(b'Prime number: ')
    pr.sendline(b'0')

pr.sendline(str(leet_prime).encode())
print(pr.recvall())