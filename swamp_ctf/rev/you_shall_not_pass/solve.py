from pwn import *

expected_result = [
  0xdd, 0x9a, 0xde, 0x4e, 0x69, 0xe1, 0xe9, 0x2c,
  0xd2, 0x4e, 0xec, 0xe7, 0x18, 0x26, 0x6a, 0x56,
  0x79, 0xd8, 0xa3, 0x55, 0x72, 0xbc, 0x76, 0xc4,
  0x0c, 0x0f, 0x9b, 0xbe, 0xc6, 0x81, 0xe2, 0x41,
  0x47, 0xa0, 0xf4, 0x26
]
eax =1
ecx = 0xc74f08c9
# edx =0
esi=1
flag = b''
for edx in range(36):
    eax = (eax*0x14a + 0x64)&0xffffffff
    rdi = eax * ecx
    rdi &= 0xFFFFFFFFFFFFFFFF
    rdi = rdi >> 32
    r8d = eax
    r8d = ((r8d - rdi) >> 1) + rdi
    r8d = r8d >> 0xb
    eax = (eax - (r8d * 0x8ff)) & 0xFFFFFFFF
    print("eax:", hex(eax&0xff))
    flag+= ((eax&0xff)^expected_result[edx]).to_bytes(1, 'big')

print("Flag:", flag)

'''
Assembly extracted form gdb:
   0x7ffff7fbc000:    push   r15
   0x7ffff7fbc002:    push   r14
   0x7ffff7fbc004:    push   r13
   0x7ffff7fbc006:    push   r12
   0x7ffff7fbc008:    push   rbx
   0x7ffff7fbc009:    mov    r15,r8
   0x7ffff7fbc00c:    mov    r12,rcx
   0x7ffff7fbc00f:    mov    rbx,rdx
   0x7ffff7fbc012:    mov    r14,rsi
   0x7ffff7fbc015:    mov    rsi,rdi
   0x7ffff7fbc018:    xor    r13d,r13d
   0x7ffff7fbc01b:    mov    edi,0x0
   0x7ffff7fbc020:    mov    edx,0x1c
   0x7ffff7fbc025:    mov    eax,0x1
   0x7ffff7fbc02a:    syscall
   0x7ffff7fbc02c:    xor    edi,edi
   0x7ffff7fbc02e:    mov    rsi,r12
   0x7ffff7fbc031:    mov    edx,0x24
   0x7ffff7fbc036:    xor    eax,eax
   0x7ffff7fbc038:    syscall
   0x7ffff7fbc03a:    mov    eax,0x1
   0x7ffff7fbc03f:    mov    ecx,0xc74f08c9
   0x7ffff7fbc044:    xor    edx,edx
   0x7ffff7fbc046:    mov    esi,0x1
   0x7ffff7fbc04b:    imul   eax,eax,0x14a
   0x7ffff7fbc051:    add    eax,0x64
   0x7ffff7fbc054:    mov    rdi,rax
   0x7ffff7fbc057:    imul   rdi,rcx
   0x7ffff7fbc05b:    shr    rdi,0x20
   0x7ffff7fbc05f:    mov    r8d,eax
   0x7ffff7fbc062:    sub    r8d,edi
   0x7ffff7fbc065:    shr    r8d,1
   0x7ffff7fbc068:    add    r8d,edi
   0x7ffff7fbc06b:    shr    r8d,0xb
   0x7ffff7fbc06f:    imul   edi,r8d,0x8ff
   0x7ffff7fbc076:    sub    eax,edi
=> 0x7ffff7fbc078:    movzx  edi,BYTE PTR [r12+rdx1]
   0x7ffff7fbc07d:    xor    dil,al
   0x7ffff7fbc080:    movzx  edi,dil
   0x7ffff7fbc084:    movsx  r8d,BYTE PTR [r15+rdx1]
   0x7ffff7fbc089:    cmp    dil,r8b
   0x7ffff7fbc08c:    cmovne esi,r13d
   0x7ffff7fbc090:    inc    rdx
   0x7ffff7fbc093:    cmp    rdx,0x24
   0x7ffff7fbc097:    jne    0x7ffff7fbc04b
   0x7ffff7fbc099:    test   esi,esi
   0x7ffff7fbc09b:    cmove  rbx,r14
   0x7ffff7fbc09f:    mov    edi,0x1
   0x7ffff7fbc0a4:    mov    rsi,rbx
   0x7ffff7fbc0a7:    mov    edx,0xa
   0x7ffff7fbc0ac:    mov    eax,0x1
   0x7ffff7fbc0b1:    pop    rbx
   0x7ffff7fbc0b2:    pop    r12
   0x7ffff7fbc0b4:    pop    r13
   0x7ffff7fbc0b6:    pop    r14
   0x7ffff7fbc0b8:    pop    r15
   0x7ffff7fbc0ba:    syscall
   0x7ffff7fbc0bc:    ret
   0x7ffff7fbc0bd:    ret
'''