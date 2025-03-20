from pwn import *

characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"
flag = ""
shifted_flag = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
not_the_flag = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"

def bigram_multiplicative_shift(bigram):
    assert(len(bigram) == 2)
    pos1 = characters.find(bigram[0]) + 1
    pos2 = characters.find(bigram[1]) + 1
    shift = (pos1 * pos2) % 67
    return characters[((pos1 * shift) % 67) - 1] + characters[((pos2 * shift) % 67) - 1]

bg_hash_map = {}
for c1 in characters:
    for c2 in characters:
        inp_bg = c1+c2
        out_bg = bigram_multiplicative_shift(inp_bg)
        if out_bg not in bg_hash_map:
            bg_hash_map[out_bg] = []
        bg_hash_map[out_bg].append(inp_bg)


for i in range(0, len(shifted_flag), 2):
    shifted_bigram = shifted_flag[i:i+2]
    un_shifted_bigram = bg_hash_map[shifted_bigram]
    not_1 = not_the_flag[i:i+2]
    not_2 = also_not_the_flag[i:i+2]
    for usb in  un_shifted_bigram:
        if usb!=not_1 and usb!=not_2:
            flag+=usb

print(flag)
