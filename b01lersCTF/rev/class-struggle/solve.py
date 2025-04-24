from pwn import *

context.binary = elf = ELF('./a.out')

def b_rev(chr,ind):
    return (chr<<(ind&7) | chr>>(8-(ind&7)))&0xFF

def 

arr = p64(0xE45C85616CBFC032)
arr += p64(0x24A7CEFA28FD040)
arr+= p64(0x3339976818379F04)
arr+= p64(0x7E068340F120F1BE)
arr+= p64(0xC3FE47A646F17E06)
arr+= p64(0x339B10BA4D0467C8)

v2=b''
for i in range(46):
    v2 += (b_rev(arr[i], i%8)^0xF).to_bytes(1, 'little')


print(v2)
