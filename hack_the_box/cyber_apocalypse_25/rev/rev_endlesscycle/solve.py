import ctypes as cts
from pwn import *
import dis

libc = cts.CDLL('libc.so.6')

libc.srand(0x0cfd2bc5b)

arr = [12, 112, 39, 232, 142, 85, 32, 673, 57, 33, 112, 814,
359, 593, 243, 489, 808, 93, 418, 742, 73, 124, 375,
97, 249, 26, 459, 336, 74, 56, 185, 42, 245, 196, 14,
349, 18, 143, 16, 380, 70, 7, 5, 703, 9, 832, 191, 105,
376, 410, 88, 665, 55, 106, 355, 65, 270, 41, 54, 559,
105, 8, 99, 198, 238, 252, 59, 91, 33, 36, 155, 66,
186, 193, 70, 614, 476, 77, 6, 35, 0, 291, 44, 66, 278,
211, 237, 214, 159, 21, 162, 233, 595, 71, 773, 292,
580, 88, 190, 27, 433, 27, 69, 39, 205, 108, 151, 743,
983, 238, 1398, 115, 271, 453, 127, 166, 197, 860, 527,
35, 334, 241, 260, 510, 15, 103, 563, 253, 260, 148,
452, 240, 140, 43, 150, 20, 200, 222, 476, 0, 311, 97,
22, 87, 614, 1101, 387, 34, 32, 214, 362, 43, 340, 165,
164, 298, 319, 738]

bytes = []
for i in range(0, len(arr)):
    bytes.append(0)
    for j in range(arr[i]):
        libc.rand()
    bytes[i] = libc.rand() & 0xff

print(bytes)
code = b''
for i in range(0, len(bytes)):
        code += (bytes[i].to_bytes(1, byteorder='big'))

# print(code)
# print(len(code))
print(disasm(code[:0x84]))
flag = code[0x84:]
xor_key = p32(0xbeefcafe)
for i in range(0, len(flag)):
     print(chr(flag[i] ^ xor_key[i % 4]), end='')
