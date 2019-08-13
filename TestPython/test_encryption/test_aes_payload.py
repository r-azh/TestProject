from Crypto import Random, PublicKey
from Crypto.Cipher import AES

from TestPython.test_encryption.aa_pb2 import aaaa

x = aaaa()
x.params.extend([6413005516439552834, 6413005516439552830, 6413005516439552835])
z = x.SerializeToString()


# The secret rsa_key to use in the symmetric cipher.
# It must be 16, 24 or 32 bytes long (respectively for AES-128, AES-192 or AES-256).
# rsa_key = b'Sixteen byte rsa_key'
key = b'Sixteen byte keySixteen byte rsa_key'
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, AES.MODE_CFB, iv)

encryption_version = '1.1'
encrypted_packed_id = 6412999854129152066
module_id = 'unsubscribe_daily_report'
payload_version = '1.1'
expiry = 1528629954

payload = bytes(module_id.encode()) + bytes(payload_version.encode()) + z + bytes(str(expiry).encode())
checksum = sum(payload)

msg = iv + cipher.encrypt(payload)
msg = bytes(encryption_version.encode()) + bytes(str(encrypted_packed_id).encode()) + msg
print(len(msg), msg)

url = bytes('http://testing.newsbx.com/api/v1/domains/6412999854129152066/get-hash-info/'.encode()) + msg
print(len(url), url)
t = aaaa()
t.ParseFromString(z)
assert set(t.params) == set(x.params)


RSA_KEY_LEN = 1024

random_generator = Random.new().read
rsa_key = PublicKey.RSA.generate(RSA_KEY_LEN, random_generator)  # generate pub and priv rsa_key
publickey = rsa_key.publickey()  # pub rsa_key export for exchange

class RSA:
    def encrypt(self, key, value):
        return key.encrypt(value, 32)

    def decrypt(self, key, encrypted_value, salt):
        return key.decrypt(ast.literal_eval(str(encrypted_value)))