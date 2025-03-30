from pwn import *
import secrets

DEATH_CAUSES = [
	'a fever',
	'dysentery',
	'measles',
	'cholera',
	'typhoid',
	'exhaustion',
	'a snakebite',
	'a broken leg',
	'a broken arm',
	'drowning',
]

def brute_force(c, n):
    '''
    brute force the message
    '''
    lives = []
    for j in DEATH_CAUSES:
        die = f'you die of {j}.'
        # print(die)
        d = int.from_bytes(die.encode(), 'big')
        l = (c-d)%n
        live = l.to_bytes((l.bit_length() + 7) // 8, 'big')
        try:
            page = int(live[35:-1].decode())
            return page
        except:
            pass
        

pr = process('server.py')
for i in range(64):
    # for i in range(10):
    pr.recvuntil(b'n: ')
    n = int(pr.recvline().strip())

    pr.recvuntil(b'e: ')
    e = int(pr.recvline().strip())

    pr.recvuntil(b'x0: ')
    x0 = int(pr.recvline().strip())

    pr.recvuntil(b'x1: ')
    x1 = int(pr.recvline().strip())

    val_send = ((x0+x1)*pow(2,-1,n))%n
    pr.recvuntil(b'v: ')
    pr.sendline(str(val_send).encode())

    pr.recvuntil(b'c0: ')
    c0 = int(pr.recvline().strip())

    pr.recvuntil(b'c1: ')
    c1 = int(pr.recvline().strip())

    # Now we can calculate the messages
    page = brute_force((c0+c1)%n,n)
    pr.sendline(str(page).encode())
print(pr.recvall().decode())