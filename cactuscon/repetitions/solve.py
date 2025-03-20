from pwn import *

def xor(data, key):
    # repeating key xor
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

pr = remote('45.55.47.125', 31243)

cipher = bytes.fromhex('250313131a5b52725c104c51584c7158404c4c5a5572565f4d590d076e58104005560321571411025a1c')
print(len(cipher))


print(xor(cipher,b'Cortana'))
