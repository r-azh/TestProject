import base64
from random import randint
from bson import ObjectId
from pymongo import MongoClient
from pyutil.cryptography.rsa.object_coder import ObjectCoder
from pyutil.cryptography.rsa.string_coder import StringCoder

__author__ = 'R.Azh'


password = 123456

object_coder = ObjectCoder("YyxuKKj7ir9NIfbM00C2DfBeTonX7t_uIAa-Vjbyqbg=")    #(Config().secret_key)
hashed_pass = object_coder.encode(password)
hashed_pass2 = object_coder.encode(password)
hashed_pass3 = object_coder.encode(password)

print(hashed_pass)
print(hashed_pass2)
print(hashed_pass3)

passwd = object_coder.decode(hashed_pass)
print(passwd)
passwd2 = object_coder.decode(hashed_pass2)
print(passwd2)

_str = 'test123456'

string_coder = StringCoder("YyxuKKj7ir9NIfbM00C2DfBeTonX7t_uIAa-Vjbyqbg=")
hashed_str = string_coder.encode(_str)
_str = string_coder.decode(hashed_str)
print(_str)

print("############## Flask bcrypt ###################")
# from flask.ext.bcrypt import Bcrypt #deprecated
from flask_bcrypt import Bcrypt
user_name = 'testuser'
user_pass = '۱۲۳۴۵۶۷۸'

dbClient = MongoClient('localhost', 27017)
db = dbClient.test_database
collection = db.users


def create_user(u_name, u_pass):
    bcrypt = Bcrypt(None)
    password_hash = bcrypt.generate_password_hash(u_pass)
    print("password_hash:", password_hash)

    post = {"_id": str(ObjectId()), "last_login": "never", "user_name": u_name, "user_pass": password_hash}

    posts = collection
    post_id = posts.insert_one(post).inserted_id
    print(post_id)


def login(u_name, u_pass):
    bcrypt = Bcrypt(None)
    if db.users.find({"user_name": u_name}).count() == 0:
        print("User %s not found" % u_name)
        logged_in = False
    else:
        cursor = db.users.find_one({"user_name": u_name})
        password = bcrypt.check_password_hash(cursor['user_pass'], u_pass)

        if password:
            print("Password accepted, authentication successfull")
            logged_in = True
        else:
            print("Password rejected. Login failed")
            logged_in = False

    return logged_in

create_user(user_name, user_pass)
print(login(user_name, user_pass))
print(login(user_name, "123456"))


print("############### bcrypt ##################")

import bcrypt
password = b"super secret password"
# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
# Hash a password for the first time, with a certain number of rounds
# hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
# Check that a unhashed password matches one that has previously been hashed
print(hashed)
if bcrypt.hashpw(password, hashed) == hashed:
    print("It Matches!")
else:
    print("It Does not Match :(")

print("############## hashlib ###################")
# used to hash the password similar to how MySQL hashes passwords with the password() function.
import hashlib
password = "654321"
hash_password = hashlib.sha1(password.encode('utf-8')).digest()
hash_password = hashlib.sha1(hash_password).hexdigest()
hash_password = '*' + hash_password.upper()
print(hash_password)


print("############## AES ###################")
from Crypto.Cipher import AES
secret_key = 'YyxuKKj7ir9NIfbM00C2DfBeTonX7t_='

# password = "12345678"
password = "1234567890123456"   # length must be multiple of 16
cipher = AES.new(secret_key)
obj_encoded = base64.b64encode(cipher.encrypt(password))
obj_decoded = base64.b64decode(cipher.decrypt(password))
print(password)

