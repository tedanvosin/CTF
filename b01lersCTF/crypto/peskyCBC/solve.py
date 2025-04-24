#!/usr/bin/env python3
from pwn import process
import sys

def main():
    # adjust this if your challenge has a different name
    p = process('./pesky_cbc.py')

    # 1) grab the ECB‐encrypted secret
    p.recvuntil(b"Here is the encrypted secret:\n")
    C_hex = p.recvline().strip()
    C = bytes.fromhex(C_hex.decode())
    print("[*] Encrypted secret (ECB):", C_hex.decode())

    # 2) skip the 8 known‐plaintext hints
    #    (each hint is two lines: plaintext, ciphertext)
    for _ in range(8):
        p.recvline()
        p.recvline()

    # 3) build your two‐block payload: 16 bytes of 0 || C
    payload = b"\x00" * 16 + C

    # 4) call pesky decrypt (option 1)
    p.recvuntil(b">> ")
    p.sendline(b"1")
    p.recvuntil(b">> ")
    p.sendline(payload.hex().encode())

    # the oracle will print you hex(CONCAT(P0',P1'))
    # where P1' == AES_CBC-1(key2, iv2, payload)[1] == AES^-1_k2(C)
    out = p.recvline().strip()
    data = bytes.fromhex(out.decode())

    # extract the second block
    secret = data[16:32]
    print("[*] Recovered secret:", secret.hex())

    # 5) submit it back (option 2) and dump the flag
    p.recvuntil(b">> ")
    p.sendline(b"2")
    p.recvuntil(b">> ")
    p.sendline(secret.hex().encode())

    # print everything the binary spits from here on
    print(p.recvall().decode())

if __name__ == "__main__":
    main()
