from sympy import primerange
import random
from collections import deque
from pwn import *
import numpy as np
from pprint import pprint

path = ""
min_xor = 100

def find_min_xor_path(a,b,grid,run_xor,run_path):
    run_xor ^= grid[a][b]
    if a==9 and b==9:
        global min_xor
        global path
        if run_xor<min_xor:
            min_xor = run_xor
            path = run_path
        return
    else:
        if a<9:
            find_min_xor_path(a+1,b,grid,run_xor,run_path+'S')
        if b<9:
            find_min_xor_path(a,b+1,grid,run_xor,run_path+'D')


def get_grid(ini_grid, mod):
    for a in list(primerange(2, 12)):
        for b in range(101):
            # Create a grid to store the n values
                n_grid = np.zeros((10, 10), dtype=int)
                all_valid = True
                
                # Set to keep track of which n values have been used
                used_n_values = set()
                
                # For each position in the grid, solve for n
                for i in range(10):
                    for j in range(10):
                        if i == 0 and j == 0:
                            continue

                        value = ini_grid[i][j]
                        
                        # Find n where (a * n + b) % mod = value
                        # Rearranging: n = ((value - b) * inverse(a)) % mod
                        
                        # Calculate (value - b) % mod
                        remainder = (value - b) % mod
                        
                        # Calculate modular multiplicative inverse of a (mod 101)
                        # Since 101 is prime, we can use Fermat's little theorem:
                        # a^(mod-1) ≡ 1 (mod mod), so a^(mod-2) ≡ a^-1 (mod mod)
                        inverse_a = pow(a, mod - 2, mod)
                        
                        # Calculate n
                        n = (remainder * inverse_a) % mod
                        
                        # Check if n is in our valid range [0-9]
                        if n > 9:
                            all_valid = False
                            break
                        
                        # Add n to our grid
                        n_grid[i][j] = n
                        used_n_values.add(n)
                    
                    if not all_valid:
                        break
                
                if all_valid and len(used_n_values) == 10 and used_n_values == set(range(10)):
                    # Verify our solution by reconstructing the grid
                    verified = True
                    for i in range(10):
                        for j in range(10):
                            if ini_grid[i][j] != (a * n_grid[i][j] + b) % mod:
                                verified = False
                                break
                        if not verified:
                            break
                    if verified:
                        print(f"Found a={a}, b={b}")
                        pprint(n_grid)
                        return n_grid

pr = remote('chals1.apoorvctf.xyz', 4002)

pr.recvuntil('\nPa ')

ini_grid = []
for i in range(10):
    ini_grid.append(pr.recvline().decode().strip().split())
print(ini_grid)
ini_grid[0] = [0] + ini_grid[0]

for i in range(10):
    for j in range(10):
        ini_grid[i][j] = int(ini_grid[i][j])

pprint(ini_grid)
mod = 101
n_grid = get_grid(ini_grid, mod)

print(n_grid)

find_min_xor_path(0,0,n_grid,0,'')
print(min_xor)
print(path)

for c in path:
    pr.sendline(c.encode())
pr.interactive()