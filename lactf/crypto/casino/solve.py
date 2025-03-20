from z3 import Int, Solver
from pwn import *
import binascii

class LCG:
    def __init__(self, a: int, c: int, m: int, seed: int):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state


def recover_lcg_seed(a, c, m, ranked_indices):
    """
    Uses Z3 solver to recover the LCG initial state (seed) from ranked indices.
    """
    solver = Solver()
    n = len(ranked_indices)

    # Create symbolic LCG outputs
    X = [Int(f"X_{i}") for i in range(n)]

    # Define the LCG recurrence relation
    for i in range(n - 1):
        solver.add(X[i + 1] == (a * X[i] + c) % m)

    # Enforce ranking constraints
    for i in range(n):
        for j in range(i + 1, n):
            if ranked_indices[i] < ranked_indices[j]:  # If original i < j
                solver.add(X[i] < X[j])  # Then LCG(i) < LCG(j)

    # Solve for initial state
    if solver.check() == "sat":
        model = solver.model()
        return model[X[0]].as_long()  # Extract recovered X_0
    else:
        print("Failed to recover LCG state.")
        return None


def reverse_shuffle(shuffled_msg, a, c, m, seed):
    """
    Reconstructs the original message by reversing the shuffle.
    """
    l = len(shuffled_msg)
    L = LCG(a, c, m, seed)
    
    positions = [L.next() for _ in range(l)]
    
    # Reverse the sorting operation
    sorted_positions = sorted(range(l), key=lambda i: positions[i])
    original_msg = bytearray(l)
    
    for i, idx in enumerate(sorted_positions):
        original_msg[idx] = shuffled_msg[i]
    
    return original_msg


pr = remote("chall.lac.tf", 31172)
# ---------------- ATTACK ----------------
# Known values from the server
pr.recvuntil(b'a=')
a = int(pr.recvline().strip(),10)

pr.recvuntil(b'c=')
c = int(pr.recvline().strip(),10)

pr.recvuntil(b'm=')
m = int(pr.recvline().strip(),10)

# Step 1: Send ordered input and get shuffled output
ordered_msg = bytes(range(256))  # 0x00, 0x01, ..., 0xFF
pr.sendline(b'1')
pr.sendline(binascii.hexlify(ordered_msg))

pr.recvuntil(b'Here you go: ')
shuffled_hex = pr.recvline().strip()
shuffled_msg = binascii.unhexlify(shuffled_hex)
print(shuffled_msg)

# Step 2: Extract ranking
ranked_indices = sorted(range(len(shuffled_msg)), key=lambda i: shuffled_msg[i])
print(ranked_indices)
# Step 3: Recover LCG seed
seed = recover_lcg_seed(a, c, m, ranked_indices)

if seed:
    print(f"Recovered LCG seed: {seed}")

    # Step 4: Reverse shuffle for the secret
    shuffled_secret_hex = input("Enter the shuffled secret (hex): ").strip()
    shuffled_secret = binascii.unhexlify(shuffled_secret_hex)
    
    original_secret = reverse_shuffle(shuffled_secret, a, c, m, seed)
    
    print(f"Recovered secret: {binascii.hexlify(original_secret).decode()}")
