from pwn import *
from Crypto.Cipher import AES

def decrypt(data,key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

key_1 = p64(0x264BC653D7BFE7F2) + p64(0x0E82884E68769F997)
key_2 = p64(0x673327922690F9DC) + p64(0x333AC75145C60824)
key_3 = p64(0x0A0407010D8CE31EE) + p64(0x0D573793257CF53D9)

dest = p64(0x0A646484365C8EB8C) + p64(0x9F803F2F42E80598) + p64(0x3ED81A287DB3C9A8) + p64(0x6CB78FE92B1ABAAA)

print(decrypt(decrypt(decrypt(dest,key_3),key_2),key_1))