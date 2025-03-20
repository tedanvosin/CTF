from pwn import *
from ctypes import CDLL
from collections import Counter
from itertools import combinations
from collections import defaultdict, OrderedDict
import random

libc = CDLL("./libc.so.6")
#pr = process('./challenge')
#pr = remote('the-thirty-twodle-challenge.chal.hackthe.vote',1337)
wordlist = []
with open('wordlist.txt','r') as file:
    for i in range(2313):
        wordlist.append(file.readline().strip())

valid_words = []
with open('valid_words.txt','r') as file:
    for i in range(12542):
        valid_words.append(file.readline().strip())


print(len(wordlist))
print(len(valid_words))

for seed in range(10000):
    libc.srand(seed+1)


    solutions=[]
    for i in range(32):
        solutions.append(wordlist[libc.rand()%0x909])

    # bad = False
    # for word in solutions:
    #     if len(set(word))!=5:
    #         bad = True
    
    # if bad==True:
    #     continue
    possible_words = ['stick','flora','debug','nymph']
    if sorted(list(set("".join(solutions)))) == sorted(list(set("".join(possible_words))))[:len(list(set("".join(solutions))))]:
        print(f"Best solution:{seed+1}:{hex(seed+1)}")
        print(f"wordlist for the seed:{(solutions)}")
        print(f"Set list for the seed:len={len(set("".join(solutions)))}\n{sorted(list(set("".join(solutions))))}\n\n")
    # if len(set("".join(solutions))) <= 20:
    #     print(f'Possible good seed:{seed+1}:{hex(seed+1)}')
    #     print(f"wordlist for the seed:{sorted(solutions)}")
    #     print(f"Set list for the seed:len={len(set("".join(solutions)))}\n{sorted(list(set("".join(solutions))))}\n\n")


