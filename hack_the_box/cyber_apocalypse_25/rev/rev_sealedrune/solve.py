from base64 import b64decode

flag = 'LmB9ZDNsNDN2M3JfYzFnNG1fM251cntCVEhgIHNpIGxsZXBzIHRlcmNlcyBlaFQ='
flag = b64decode(flag)
print(flag[::-1])


