import hashlib
from Crypto.Util.number import bytes_to_long
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192
import random
import time
import json

FLAG = "flag{fake-flag-for-testing}"
s = generator_192.order()

secret = random.randrange(1, s)
pubkey = Public_key(generator_192, generator_192 * secret)
privkey = Private_key(pubkey, secret)
r = random.Random()

def signature():
    text = f"Current time is {time.strftime('%H:%M:%S')}"
    hsh = hashlib.sha1(text.encode()).digest()
    sig = privkey.sign(bytes_to_long(hsh), r.getrandbits(192))
    return {"msg": text, "r": hex(sig.r), "s": hex(sig.s)}

def verify(msg: str, sig_r: str, sig_s: str):
    hsh = bytes_to_long(hashlib.sha1(msg.encode()).digest())
    sig_r = int(sig_r, 16)
    sig_s = int(sig_s, 16)
    sig = Signature(sig_r, sig_s)

    if pubkey.verifies(hsh, sig):
        return True
    else:
        return False

print("""
      Welcome to FRNG Curves...\n
      """)
print("1. Get a fully random signature")
print("2. Verify a signature")
print("3. Give me random!")

while True:
    try:
        choice = int(input("\nEnter your option: "))
    except:
        break

    if choice == 1:
        print(signature())
    elif choice == 2:
        data = json.loads(input("Enter 'msg', 'r' and 's' in json format: "))
        msg = data['msg']
        r = data['r']
        s = data['s']
        verified = verify(msg, r, s)

        if verified and msg == "open seasame":
            print("flag =", FLAG)
            break
        elif verified:
            print("Message verified")
        else:
            print("Bad signature")
    elif choice == 3:
        print("Here's some random bits to cheer you up:", r.getrandbits(32))
    else:
        break
