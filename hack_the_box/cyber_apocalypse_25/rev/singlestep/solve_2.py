from pwn import *


inp_matrix = [88,-17,19,-57,
              45,-9,10,-29,
              -56,11,-12,36,
              -40,8,-9,26]

inv_matrix = [1,5,2,5,
              4,8,7,8,
              2,8,6,5,
              1,8,3,7]

key=''
for i in range(len(inv_matrix)):
    if i%4==0 and len(key)>0:
        key+='-'
    key+=chr(inv_matrix[i]+ord('A')+((i//4)*(i%4)))

pr=process('./singlestep')
pr.sendline(key.encode())
print(pr.recvall().decode())