#!/usr/bin/env python3
from Crypto.Util.number import long_to_bytes
from pwn import *
import sys

def crt(primes, residues):
    """
    Solve x ≡ residues[i] (mod primes[i]) for i=0..n-1
    Returns the unique x modulo (product of all primes).
    """
    P = 1
    for p in primes:
        P *= p

    x = 0
    for p, r in zip(primes, residues):
        m = P // p
        inv = pow(m, -1, p)
        x += r * inv * m

    return x % P

def main(runs=20):
    primes = []
    residues = []

    for i in range(runs):
        # pr = process('ASSS.py')
        pr = remote('asss.atreides.b01lersc.tf', 8443,ssl=True)
        # read prime 'a'
        pr.recvuntil(b"Here is a ^_^: ")
        a_line = pr.recvline().strip()
        a = int(a_line, 0)
        print(f"[{i+1}/{runs}] a = {hex(a)}")

        # read share tuple "(share, value)"
        pr.recvuntil(b"Here is your share ^_^: (")
        share_value_line = pr.recvline().strip()
        if share_value_line.endswith(b")"):
            share_value_line = share_value_line[:-1]
        share_str, value_str = share_value_line.split(b", ")
        share = int(share_str, 0)
        value = int(value_str, 0)
        print(f"    share = {share}, value = {value}")

        # compute residue r = value mod a
        r = value % a
        print(f"    residue (s mod a) = {hex(r)}\n")

        primes.append(a)
        residues.append(r)

    # reconstruct s via CRT
    s = crt(primes, residues)
    try:
        flag = long_to_bytes(s).decode()
    except:
        flag = long_to_bytes(s)

    print("Recovered secret integer (s):", s)
    print("Recovered flag:", flag)

if __name__ == "__main__":
    # optionally accept number of runs via command-line
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    main(runs)
