import os
import requests
from Cryptodome.Cipher import AES
import hashlib

def get_nonce():
    while True:
        nonce = os.urandom(16)
        # Check if first 3 bytes of sha256(b'pow/' + nonce) are zero
        if hashlib.sha256(b'pow/' + nonce).digest()[:3] == b'\x00\x00\x00':
            return nonce

print("What is the flag?> ")
flag = input().encode()

nonce = get_nonce()
r = requests.post(
    'https://c12-cypress.hkcert24.pwnable.hk/',
    json={'nonce': nonce.hex()}
)
print(r.text)

# Get ciphertext from response
c0 = bytes.fromhex(r.text)
print(len(r.text))
# Generate key and IV from nonce
key = hashlib.sha256(b'key/' + nonce).digest()[:16]
iv = hashlib.sha256(b'iv/' + nonce).digest()[:16]
print(key.hex())
print(iv.hex())
# Create cipher and encrypt flag
cipher = AES.new(key, AES.MODE_CFB, iv)
#c1 = cipher.encrypt(flag)
print(cipher.decrypt(c0))
# Compare results and print emoji
#print('🙆🙅'[c0 != c1])


