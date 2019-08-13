import base64
import binascii
import codecs
import hashlib


key = 'user1.team1.inbox1'
salt = 'salty'

hash = hashlib.md5((salt + key).encode('utf-8')).hexdigest()

print(hash)

# MD5 is no longer considered safe for password storage. Consider instead scrypt, bcrypt, or PBDKF2
import bcrypt
salt = bcrypt.gensalt()
print(salt)
hash = bcrypt.hashpw(key.encode('utf-8'), salt)
print(hash)
print(hash.decode())

salt = 'new salty'
salt_hex = bytes(salt.encode('utf-8')).hex()
print(salt_hex)
bcrypt_salt = "$2a$12$" + base64.b64encode(binascii.a2b_hex(("0" * 32 + salt_hex)[-32:])).decode()
print(bcrypt_salt)
hash = bcrypt.hashpw(key.encode('utf-8'), bcrypt_salt.encode())
print(hash)
print(hash.decode())

# convert bytes to string
#  bytes_obj.decode()

# convert string to bytes
# bytes(str_obj)


def generate_hash_with_salt(plain_text, salt=None, salt_length=32, hash_max_length=100, prepare_for_url=True):
    plain_text = plain_text.encode()
    salt_hex = bytes(salt.encode()).hex()
    bcrypt_salt = ("$2a$12$" + base64.b64encode(binascii.a2b_hex(("0" * 32 + salt_hex)[-32:])).decode()).encode()
    hash = bcrypt.hashpw(plain_text, bcrypt_salt)
    if prepare_for_url:
        hash = hash.decode().replace('/', '')
    return hash if len(hash) < hash_max_length else hash[:hash_max_length]


for x in range(1000):
    generate_hash_with_salt()
