from hashlib import sha256

class Account:
    def __init__(self, username="default-user", passwd=""):
        self.username = username
        self.password = sha256(passwd.encode()).digest()
        self.k_max = int(len(self.username) ** 6)
        if self.k_max < 65536:
            self.k_max += 1000000
        self.stored_msgs = 0

    def login(self, pw=None):
        if not pw:
            pw = input("Enter your password : ")
        return sha256(pw.encode()).hexdigest() == self.password.hex()