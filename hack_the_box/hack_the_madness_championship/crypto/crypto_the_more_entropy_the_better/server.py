import os, re
from secrets import randbelow, choice
from ecdsa import SigningKey, BRAINPOOLP384r1
from hashlib import sha384

# the publicly accessible fingerprint dataset "SOCOFing"
# https://www.kaggle.com/datasets/ruizgara/socofing
DATASET_DIR = 'SOCOFing'
REAL_DIR = DATASET_DIR+'/Real/'
ALTERED_DIR = DATASET_DIR+'/Altered/Altered-Hard/'
CHOSEN_FINGER = 'Right_thumb'
EMPLOYEES_NUM = 600
ADMIN = 137

def read_employee_fingerprints(dirname):
    return [dirname + fn for fn in list(filter(lambda fn: CHOSEN_FINGER in fn, os.listdir(dirname)))]

def get_fingerprint_file_from_employee_id(eid):
    return list(filter(lambda rf: str(eid) in rf, real_fingerprints))[0]

real_fingerprints = read_employee_fingerprints(REAL_DIR)
admin_fingerprint_file = get_fingerprint_file_from_employee_id(ADMIN)
altered_fingerprints = read_employee_fingerprints(ALTERED_DIR)

class FingSign:
    def __init__(self):
        self.signing_key = SigningKey.generate(curve=BRAINPOOLP384r1)
        self.n = BRAINPOOLP384r1.order
        self.entropy = [randbelow(self.n)]

    def test_signing_service(self):
        for _ in range(10):
            altered_fingerprint = choice(altered_fingerprints)
            sig, file_hash = self.fingerprint_sign(altered_fingerprint)
            assert self.verify_fingerprint_signature(altered_fingerprint, sig)
            print(f'Signature {sig.hex()} verified for file {file_hash} !')

    def fingerprint_sign(self, fingerprint_file):
        fingerprint_data = open(fingerprint_file, 'rb').read()
        h = sha384(fingerprint_file.encode()).hexdigest()
        sig = self.signing_key.sign(fingerprint_data, hashfunc=sha384, k=sum(self.entropy)%self.n)
        # increase entropy
        self.entropy *= 2
        return sig, h

    def verify_fingerprint_signature(self, fingerprint_file, sig):
        fingerprint_data = open(fingerprint_file, 'rb').read()
        verifying_key = self.signing_key.verifying_key
        return verifying_key.verify(sig, fingerprint_data, hashfunc=sha384)

    def check_admin(self):
        input_sig = bytes.fromhex(input(f'[+] Please provide the admin fingerprint signature (in hex) :: '))
        return self.verify_fingerprint_signature(admin_fingerprint_file, input_sig)


def show_menu():
    print('''
    [1] Test signing service using altered fingerprints
    [2] Enter as admin via fingerprint authentication
    [3] Exit
    ''')

def main():
    fingsign = FingSign()

    while True:
        show_menu()
        choice = input('> ')
        if choice == '1':
            fingsign.test_signing_service()
        elif choice == '2':
            verified = fingsign.check_admin()
            if verified:
                print(f'[AUTHORIZED] Welcome admin! Here is your flag :: {open("flag.txt").read()}')
            else:
                print('[UNAUTHORIZED] Your signature could not be verified!')
        elif choice == '3':
            print('Thank you for using our service! Make sure you leave a feedback so we can improve in the future.')
            exit()
        else:
            print('Unknown option')

main()
