from hashlib import md5

FLAG = b'flag{fake-flag-for-testing}'

print('''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠠⠄⣀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣻⡧⢤⣤⣴⣵⣄⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣻⡿⠟⠛⠉⠀⣲⣿⢂⠘⡏⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⡇⢀⣀⣠⠴⠛⣻⣿⣦⣾⡔⠠⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠛⠉⣤⣶⣿⡿⠟⣻⡿⠤⡀⠘⠄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢌⣤⣾⡿⢛⣦⣶⣵⠡⠤⠸⢣⡘⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⡎⢀⣿⢠⡟⠀⠀⠀⠀⠠⢡⡅
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠌⠀⠣⣾⡇⢸⠷⣤⢀⣤⣤⠀⣾⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠒⢰⡿⢻⣴⡎⠀⡏⡇⠁⠈⢀⠷⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⢱⢈⠱⢿⢟⡇⢸⠈⡄⠀⠐⠊⣥⠇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⡖⢟⠠⡀⠑⡀⡖⢊⣈⡍⢿⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀⣾⣩⢿⠆⠚⠉⠉⠉⠉⡻⢃⠄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣏⣿⣿⢷⠮⢦⡀⠀⢀⣔⣰⠋⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⠿⢋⡗⠁⢀⢾⡇⣀⣎⢼⠉⡀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⡥⡪⠏⠀⡰⡑⣸⣠⣾⣅⠸⡆⢡⠀
⠀⠀⠀⠀⠀⢀⣠⢾⣽⣿⢟⣴⣷⣧⣐⣯⣦⠜⠵⣄⣿⡇⠈⡜⠀
⠀⠀⠀⠀⡠⢚⣵⡿⢏⣴⢋⣿⠨⣽⣿⣿⡃⠀⠀⠈⢿⡇⣜⣠⠀
⠀⢀⣠⣾⣷⣿⢯⣴⣿⣿⣦⣜⣸⣿⡿⣿⠁⠩⠀⡌⠀⣷⣿⡞⠂
⢀⣼⠿⣿⠟⣣⡾⠻⠽⠋⠙⣻⣿⣿⡗⠛⣿⠋⠈⠀⢠⣿⣿⣿⢂
⠀⠁⠽⠃⠾⠋⠀⠀⠀⠀⢰⣿⣿⣿⡷⣶⠎⠀⠀⣠⣿⠿⠿⢿⣷
''')

print("Decrypt the artifact's data... again.\n")


def xor(a, b):
    return bytes([i ^ j for i, j in zip(a, b)])

while True:
    try:
        print("1 - Receive checksum")
        print("2 - Exit")
        choice = int(input("> "))
    except:
        break

    if choice == 1:
        message = input("Enter your message: ").encode()
        hash = md5(xor(message, FLAG)).hexdigest()
        print(f"Hash: {hash}\n")
    else:
        print("Good Bye")
        break