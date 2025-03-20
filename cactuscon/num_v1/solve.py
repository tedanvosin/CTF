from pwn import *
import ctypes as cts
from time import time

context.binary = elf = ELF('chal')
#pr = process()
pr = remote('64.225.9.32', 31696)
libc = cts.CDLL('libc.so.6')

curr_time = time()

#libc.srand(int(curr_time))
rand_num = libc.rand() << 32
rand_num |= libc.rand()

print(rand_num)

#libc.srand(int(curr_time)-1)
#rand_num = libc.rand() << 32
#rand_num |= libc.rand()

#print(rand_num)

#libc.srand(int(curr_time)+1)
#rand_num = libc.rand() << 32
#rand_num |= libc.rand()

print(rand_num)
pr.interactive()