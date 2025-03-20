import random
from Crypto.PublicKey import DSA as PrimeGenerator

class DSA:
    def __init__(self, key_size=2048):
        key = PrimeGenerator.generate(key_size)
        self.p, self.q = key.p, key.q
        self.x, self.y, self.g = self.generate_keys()
        self.k_min = 65500

    def get_public_params(self):
        return (self.p, self.q, self.g)

    def generate_keys(self):
        h = random.randint(2, self.p-2)
        g = pow(h, (self.p-1)//self.q, self.p)
        x = random.randint(1, self.q-1)
        y = pow(g, x, self.p)
        return x, y, g

    def sign(self, h, k_max):
        k = random.randint(self.k_min, k_max)
        r = pow(self.g, k, self.p) % self.q
        s = (pow(k, -1, self.q) * (int(h, 16) + self.x * r)) % self.q
        return (r, s)

    def verify(self, h, signature):
        r, s = signature
        r = int(r)
        s = int(s)
        w = pow(s, -1, self.q)
        u1 = (int(h, 16) * w) % self.q
        u2 = (r * w) % self.q
        v = ((pow(self.g, u1, self.p) * pow(self.y, u2, self.p)) % self.p) % self.q
        return r == v