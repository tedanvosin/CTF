inp=b''
with open('flag_output','rb') as file:
    inp = file.read()

def mycipher(myinput,myletter):
    rawdecrypt = bytearray(myinput)
    print(rawdecrypt)
    flag = ''
    for iter in range(0,len(rawdecrypt)):
        flag += chr(rawdecrypt[iter] + ord(myletter))
        myletter = chr(ord(myletter) + 1)
    #encrypted = "".join(rawdecrypt)
    print("NICC{" + flag + "}")

for i in range(100):
    mycipher(inp,chr(i))
    