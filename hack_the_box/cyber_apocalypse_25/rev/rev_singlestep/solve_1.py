from pwn import *

context.binary = elf = ELF('singlestep')

binary = b''
with open('singlestep', 'rb') as f:
    binary = f.read()

f = open('disasm.txt','a')

to_be_processed = [0x1820,0x1B00,0x1CA0,0x2180,0x2630,0x3690,0x38A0,0x3ea0,0x3fc0]
processed = []

while(len(to_be_processed)>0):
    start = to_be_processed.pop(0)
    processed.append(start)
    print(f'starting to process({hex(start)})')

    code_1 = bytearray(binary[start:])
    inst=0
    pop_cnt=1
    ln = ''
    while 'ret' not in ln:
        ln = disasm(code_1,byte=False,vma=start).splitlines()
        if inst>=len(ln):
            break
        ln = ln[inst]
        # print(ln)
        if 'xor' in ln and 'rip' in ln:
            ln = list(filter(None,ln.split(' ')))
            # print(ln)
            curr_rip = int(ln[0][:-1],16)
            target_rip = int(ln[-1],16)
            if(curr_rip>target_rip):
                inst+=1
                continue
            xor_val = int(ln[-3],16)
            # print(hex(xor_val))
            for i in range(8):
                code_1[target_rip-start+i] ^= p64(xor_val)[i]
        
        elif 'pop' in ln:
            pop_cnt+=1

        elif pop_cnt==2 or 'ret' in ln:
            print(ln)
            f.write(ln.strip()+'\n')
            pop_cnt=0
                # print(ln)
        inst+=1
    f.write('\n')

