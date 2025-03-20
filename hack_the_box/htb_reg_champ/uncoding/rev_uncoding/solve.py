from pwn import *

inp = p64(0xC3E2AF1E8EDAD4C6) + p64(0xEE602548C0D4060C)
flag = p64(0x9CD1C12EF598808E) + p64(0x8A545517F3B93778) + p64(0x0AED3DB41BEADA099) + p64(0x86147A2CF4A4593F) + p64(0x0F08F9E6AD1E9E7B4) + p64(0x934E0B66A4E07653)
print(inp)

out = b''
for j in range(len(flag)):
    out += bytes([inp[j%16] ^ flag[j]])

# for i in range(256):
print(out)