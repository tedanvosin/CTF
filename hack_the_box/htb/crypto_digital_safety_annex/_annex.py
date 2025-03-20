from hashlib import sha256
from _dsa import DSA
from _account import Account

class Annex:
    def __init__(self):
        self.user_log = []
        self.users = {}
        self.vault = {}
        self.dsa = DSA()

    def create_account(self, username="", password=""):
        if (username == "" and password == ""):
            print("\n[+] Thank you for choosing the Digital Safety Annex!")
            username = input("\n[+] To get started, please enter your username: ")
            if username in self.users.keys():
                print("\n[!] Username already exists!")
                return
            password = input("[+] Next, enter your password: ")
        account = Account(username, password)
        self.users[username] = account
        return username

    def log_info(self, account, msg, h, sig):
        _id = account.stored_msgs
        if account.username not in self.vault:
            self.vault[account.username] = []
        
        self.vault[account.username].append((h, msg, (str(sig[0]), str(sig[1]))))
        self.user_log.append((sig, h))
        account.stored_msgs += 1

    def sign(self, username, message, password=""):
        account = self.users[username]
        
        if not account.login(password):
            print("[!] Invalid Password!\n")
            return (0, 0)

        msg = message.encode()
        h = sha256(msg).hexdigest()
        
        r, s = self.dsa.sign(h, account.k_max)
        
        self.log_info(account, msg, h, (r, s))
        
        return (r, s)

    def verify(self, message, signature):
        msg = message.encode()
        h = sha256(msg).hexdigest()
        return self.dsa.verify(h, signature)

    def download(self, priv, nonce, req_id, username):
        h, m, sig = self.vault[username][req_id]
        
        p, q, g = self.dsa.get_public_params()
 
        rp = pow(g, nonce, p) % q
        sp = (pow(nonce, -1, q) * (int(h, 16) + priv * rp)) % q

        new_sig = (str(rp), str(sp))

        if new_sig == sig:
            print(f"[+] Here is your super secret message: {m}")
        else:
            print(f"[!] Invalid private key or nonce value! This attempt has been recorded!")