from pwn import *

m1_enc = open('Captured_comms/M1/encrypted.txt','r').read().strip()
m1_dec = open('Captured_comms/M1/decrypted.txt','r').read().strip()
m2_enc = open('Captured_comms/M2/encrypted.txt','r').read().strip()
m2_dec = open('Captured_comms/M2/decrypted.txt','r').read().strip()
m3_enc = open('Captured_comms/M3/encrypted.txt','r').read().strip()
m3_dec = open('Captured_comms/M3/decrypted.txt','r').read().strip()
m4_enc = open('Captured_comms/M4/encrypted.txt','r').read().strip()
m4_dec = open('Captured_comms/M4/decrypted.txt','r').read().strip()
m5_enc = open('Captured_comms/M5/encrypted.txt','r').read().strip()
m5_dec = open('Captured_comms/M5/decrypted.txt','r').read().strip()

m1_enc = int(m1_enc, 2).to_bytes(len(m1_enc)//8, 'big')
m1_dec = int(m1_dec, 2).to_bytes(len(m1_dec)//8, 'big')

m2_enc = int(m2_enc, 2).to_bytes(len(m2_enc)//8, 'big')
m2_dec = int(m2_dec, 2).to_bytes(len(m2_dec)//8, 'big')

m3_enc = int(m3_enc, 2).to_bytes(len(m3_enc)//8, 'big')
m3_dec = int(m3_dec, 2).to_bytes(len(m3_dec)//8, 'big')

m4_enc = int(m4_enc, 2).to_bytes(len(m4_enc)//8, 'big')
m4_dec = int(m4_dec, 2).to_bytes(len(m4_dec)//8, 'big')

m5_enc = int(m5_enc, 2).to_bytes(len(m5_enc)//8, 'big')
m5_dec = int(m5_dec, 2).to_bytes(len(m5_dec)//8, 'big')
print("Length of M1 enc:", len(m1_enc))
print("Length of M1 dec:", len(m1_dec))
print("Length of M2 enc:", len(m2_enc))
print("Length of M2 dec:", len(m2_dec))
print("Length of M3 enc:", len(m3_enc))
print("Length of M3 dec:", len(m3_dec))
print("Length of M4 enc:", len(m4_enc))
print("Length of M4 dec:", len(m4_dec))
print("Length of M5 enc:", len(m5_enc))
print("Length of M5 dec:", len(m5_dec))

ln = b''
for i in range(len(m1_enc)):
    ln+=(m1_enc[i]^m1_enc[len(m1_enc)-1-i]).to_bytes(1, 'big')

print(ln)
ln = b''
for i in range(len(m2_enc)):
    ln+=(m1_enc[i]^m2_enc[i]).to_bytes(1, 'big')

print(ln)

# ln = []
# for i in range(len(m3_enc)):
#     ln+=(m3_dec[i]^m3_enc[i]).to_bytes(1, 'big')

# print(ln)

# ln = []
# for i in range(len(m4_enc)):
#     ln+=(m4_dec[i]^m4_enc[i]).to_bytes(1, 'big')

# print(ln)

# ln = []
# for i in range(len(m5_enc)):
#     ln+=(m5_dec[i]^m5_enc[i]).to_bytes(1, 'big')

# print(ln)