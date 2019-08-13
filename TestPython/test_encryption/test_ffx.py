# Format-preserving, Feistel-based encryption (FFX)

import pyffx
e = pyffx.Integer(b'secret-rsa_key', length=4)
x = e.encrypt(1001)
print(x)

y = e.decrypt(x)
print(y)

e = pyffx.String(b'secret-rsa_key', alphabet='abcdefghij', length=6)
x = e.encrypt('jibabc')
print(x)

y = e.decrypt(x)
print(y)
