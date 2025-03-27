from base64 import b64decode
enc_flag = "LmB9ZDNsNDN2M3JfYzFnNG1fM251cntCVEhgIHNpIGxsZXBzIHRlcmNlcyBlaFQ="

print(b64decode(enc_flag).decode('utf-8')[::-1])
