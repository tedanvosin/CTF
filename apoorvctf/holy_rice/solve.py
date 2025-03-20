from pwn import *

final_str = list("6!!sbn*ass%84z@84c(8o_^4#_#8b0)5m_&j}y$vvw!h")
other_str = "0123456789abcdefghijklmnopqrstuvwxyz_{}"

final_str = final_str[::-1]

print(final_str)
flag = ''

i =0 
while i< len(final_str):
    if len(flag)%3== 1:
        i+=1
    flag += final_str[i]
    i+=1

final_str = list(flag)

for i in range(0, len(final_str)):
    for j in range(len(other_str)):
        if final_str[i] == other_str[j]:
            final_str[i] = other_str[(j-7)%0x27]
            break

print("".join(final_str))