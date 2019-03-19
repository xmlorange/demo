# -*- coding: utf-8 -*-

import requests
import  json

TOKEN = ''

r = requests.get('https://api.github.com/users/ziqing27')
with open('res_content.txt', 'wb') as f:
    f.write(r.content)
print(r.status_code)
print(r.text)
print(r.url)
print(r.json())

