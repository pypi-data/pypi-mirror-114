'''updrage_packages
13:42 2021/7/30
updrage your all python packages!'''
import os
a=os.popen('pip list').read()
b=list(a)
c=[]
for s in b:
    if s != '-':
        c.append(s)
m=''.join(c)
import re
w=re.findall(r'[a-zA-Z]{1,100} ',''.join(c))
z=[]
for a in w:
    z.append(a[:-1])
z=z[1:]
for pack in z:
    a=os.popen('pip install -U ' + pack)
    print('success updrage package ' + pack + ':' + a.read())