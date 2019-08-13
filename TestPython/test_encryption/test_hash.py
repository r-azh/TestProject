import abc
import base64
import binascii
import hashlib
import os
import sys
from datetime import datetime
from random import randint

import bcrypt
import psycopg2

sys.path.append('/home/newshub/repositories/TestProjects')


from TestPython.test_encryption.test_encrypt import Profiler


class Hash:
    def __init__(self, algorithm):
        self.algorithm = algorithm()

    def hash(self, plain_text, salt=None):
        return self.algorithm.hash(plain_text, salt)


class HashAlgorithm(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def hash(self, plain_text, salt):
        pass


class BCrypt(HashAlgorithm):
    def hash(self, plain_text, salt):
        if salt is not None:
            salt_hex = bytes(salt.encode()).hex()
            bcrypt_salt = (
                        "$2a$12$" + base64.b64encode(binascii.a2b_hex(("0" * 32 + salt_hex)[-32:])).decode()
            ).encode()

        else:
            bcrypt_salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_text.encode(), bcrypt_salt)


# https://docs.python.org/2/library/hashlib.html
class SHA512(HashAlgorithm):
    key_length = 32
    iterations = 10

    def hash(self, plain_text, salt):
        if salt is None:
            salt = os.urandom(self.key_length)
        return hashlib.pbkdf2_hmac(
            hash_name='sha512',
            password=bytes(plain_text.encode()),
            salt=salt,
            iterations=self.iterations,
            dklen=self.key_length
        )


class SHA256(HashAlgorithm):
    key_length = 32
    iterations = 10

    def hash(self, plain_text, salt):
        if salt is None:
            salt = os.urandom(self.key_length)
        return hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=bytes(plain_text.encode()),
            salt=salt,
            iterations=self.iterations,
            dklen=self.key_length
        )


def store_in_db(hash_, module_id, user_id):
    conn = psycopg2.connect(database='pandora-test', user='postgres', host='10.0.0.6', password='HD2w2MZQTURv9w7EgNP6tj84')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO test_hash(hash, create__ts, expire__ts, module_id, user_id) "
                f"VALUES('{hash_}', '{datetime.utcnow()}'::date, '{datetime.utcnow()}'::date, {module_id}, {user_id})")
    conn.commit()


if __name__ == "__main__":
    start = datetime.utcnow()

    module_id = 6413005516439552834
    user_id = 6413002865639424514

    plain_text = f'{module_id}{user_id}'
    # print(len(plain_text))

    profiler = Profiler('hashing', print_=True)

    # for i in range(10000):
    #     profiler.push('bcrypt')
    #     hasher = Hash(BCrypt)
    #     hash = hasher.hash(plain_text)
    #     profiler.pop()
    #
    # profiler.flush()
    # print(len(hash))
    # print(hash)
    from urllib import parse

    for i in range(100):
        for j in range(1000):
            profiler.push('sha512')
            hasher = Hash(SHA512)
            hash = hasher.hash(plain_text)
            store_in_db(hash.hex(), module_id, user_id)
            profiler.pop()
    print(len(hash))
    # print(hash)
    # hash_str = parse.quote_from_bytes(hash)
    # print(hash_str)
    # print(len(hash_str))
    # profiler.flush()
    # unquote = parse.unquote_to_bytes(hash_str)
    # assert hash == unquote
    #
    # profiler.push('sha256')
    # hasher = Hash(SHA512)
    # hash = hasher.hash(plain_text)
    # profiler.pop()
    # print(hash)







