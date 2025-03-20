from secret import FLAG, HTB_PASSWD
from _annex import Annex
import re

def show_menu():
    return input("""
Welcome to the Digital Safety Annex!
We will keep your data safe so you don't have to worry!

[0] Create Account 
[1] Store Secret
[2] Verify Secret
[3] Download Secret
[4] Developer Note
[5] Exit

[+] Option > """)

def input_number(prompt):
    n = input(prompt)
    return int(n) if n.isdigit() else None

def main():
    annex = Annex()
    annex.create_account("Admin", "5up3r_53cur3_P45sw0r6")
    annex.create_account("ElGamalSux", HTB_PASSWD)
    annex.sign("ElGamalSux", "DSA is a way better algorithm", HTB_PASSWD)
    annex.sign("Admin", "Testing signing feature", "5up3r_53cur3_P45sw0r6")
    annex.sign("ElGamalSux", "I doubt anyone could beat it", HTB_PASSWD)
    annex.sign("Admin", "I should display the user log and make sure its working", "5up3r_53cur3_P45sw0r6")
    annex.sign("ElGamalSux", "To prove it, I'm going to upload my most precious item! No one but me will be able to get it!", HTB_PASSWD)
    annex.sign("ElGamalSux", FLAG, HTB_PASSWD)

    account_username = ""

    while True:
        user_inp = show_menu()
        
        if user_inp == '0':
            account_username = annex.create_account()
        
        elif user_inp == '1':
            if not account_username:
                print("\n[!] You need to create an account with the Annex first before you can store any secrets!")
            else:
                while True:
                    message = input("\nPlease enter you super secret message: ")
                    r, s = annex.sign(account_username, message)

                    if r > 0 and s > 0:
                        break

                print(f"\n[+] Here is your signature (r, s): ({r}, {s})")
                print("Keep your signature safe!!")
        
        elif user_inp == '2':
            signature = input("\nPlease enter the signature (r,s) separated by a comma: ")
            signature = re.search(r'^(\d+),(\d+)$', signature)

            if not signature:
                print("\n[!] Sorry, need a valid signature to verify message!")
                continue
            
            message = input("\nPlease enter the message you wish to verify: ").strip()
            if not message:
                print("\n[!] Sorry, need a valid message to continue verification!")
                continue

            signature = (int(signature.group(1)), int(signature.group(2)))

            if annex.verify(message, signature):
                print("[+] Message has been successfully verified!")
            else:
                print("[!] Message could not be verified! Please make sure your signature and messages are correct!")

        elif user_inp == '3':
            uname = input("\nPlease enter the username that stored the message: ")
            if not uname in annex.vault:
                print("\n[!] Sorry, need valid existing username to download secret!")
                continue

            req_id = input("\nPlease enter the message's request id: ")
            if not req_id.isdigit() or not (0 <= int(req_id) < len(annex.vault[uname])):
                print("\n[!] Sorry, need valid request id to download secret!")
                continue
            
            req_id = int(req_id)
            if uname == account_username:
                account = annex.users[account_username]

                if account.login():
                    h, msg, sig = annex.vault[uname][req_id]
                    print(f"\n[+] Here is your message: {msg}")
                else:
                    print("[-] Invalid username and/or password!")
            else:
                k = input_number("\nPlease enter the message's nonce value: ")
                if not k:
                    print("\n[!] Sorry, need a valid nonce to download secret!")
                    continue
            
                x = input_number("\n[+] Please enter the private key: ")
                if not x:
                    print("\n[!] Sorry, need a valid private key to download secret!")
                    continue

                annex.download(x, k, req_id, uname)
        
        elif user_inp == '4':
            print("\nWe are here to prove that DSA is waaayyyy better than El Gamal!\nWe also modified our signature algorithm to use the super secure SHA-256. No way you can bypass our authentication. If you must try, be sure to bring tissues for your tears of failure.\nI'll throw you a bone, these are public record anyway:\n")

            p, q, g = annex.dsa.get_public_params()

            print(f'{p = }')
            print(f'{q = }')
            print(f'{g = }')

            inp = input("[+] Test user log (y/n): ").lower()
            if inp == 'y':
                if annex.users['Admin'].login():
                    print(f'\n{annex.user_log}')
        
        elif user_inp == '5':
            print("[!] Leaving the Annex. Thanks for choosing DSA!")
            break
        
        else:
            print("[!] Invalid option.")


if __name__ == "__main__":
    main()
