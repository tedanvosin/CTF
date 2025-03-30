#''.join([chr( (ord(flag[i])<<8) + ord(flag[i+1])) for i in range(0,len(flag),2)])

flag = open('enc','rb').read()

print(len(flag))
#print(''.join([chr( ((flag[i]<<8) + flag[i+1]) & 0xff) for i in range(0,len(flag),2)]))
for i in range(0,len(flag),2):
    print(flag[i])
    #''.join([chr( (ord(flag[i])<<8) + ord(flag[i+1])) for i in range(0,len(flag),2)])
