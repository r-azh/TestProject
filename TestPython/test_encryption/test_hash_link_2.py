import abc
import binascii
import hashlib
import os
import datetime
from urllib import parse

import psycopg2


class Hash:
    def __init__(self, algorithm):
        self.algorithm = algorithm()

    def hash(self, plain_text, salt=None):
        return self.hash_with_salt(plain_text, salt)[0]

    def hash_with_salt(self, plain_text, salt=None):
        hash_result, salt = self.algorithm.hash(plain_text, salt)
        return binascii.hexlify(hash_result), salt


class HashAlgorithm(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def hash(self, plain_text, salt):
        pass


class SHA512(HashAlgorithm):
    key_length = 32
    iterations = 100000

    def hash(self, plain_text, salt=None):
        if salt is None:
            salt = hashlib.sha256(os.urandom(self.key_length)).hexdigest().encode('ascii')
        return hashlib.pbkdf2_hmac(
            hash_name='sha512',
            password=bytes(plain_text.encode('utf-8')),
            salt=salt,
            iterations=self.iterations,
            dklen=self.key_length
        ), salt


def store_in_db(hash_, module_id, user_id):
    conn = psycopg2.connect(database='test', user='postgres', host='10.0.0.6', password='HD2w2MZQTURv9w7EgNP6tj84')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO test_hash(hash, create_ts, expiry_ts, usage_limit, usage_remaining, "
                f"module_id, user_id) "
                f"VALUES('{hash_}', '{datetime.datetime.utcnow()}'::date, "
                f"'{datetime.datetime.utcnow() + datetime.timedelta(days=100)}'::date, 5, 5, "
                f"'{module_id}', {user_id})")
    conn.commit()


def get_hash_from_link_hash(hash_with_salt):
    parse.unquote(hash_with_salt)
    salt = hash_with_salt[:64]
    hash = hash_with_salt[64:]
    hasher = Hash(SHA512)
    new_hash = hasher.hash(hash, salt.encode('ascii'))
    return new_hash


def prepare_hash_for_link(hash, salt):
    return parse.quote((salt + hash).decode('ascii'))


if __name__ == "__main__":
    module_id = 6413005516439552834
    user_id = 6413002865639424514

    plain_text = f'{module_id}{user_id}'

    hasher = Hash(SHA512)
    generated_hash_for_link = hasher.hash(plain_text)

    hash_for_store_in_db, salt = hasher.hash_with_salt(generated_hash_for_link.decode('ascii'))
    hash_str = prepare_hash_for_link(generated_hash_for_link, salt)

    hash_for_store_in_db = hash_for_store_in_db.decode()
    store_in_db(hash_for_store_in_db, module_id, user_id)

    retrieved_hash = get_hash_from_link_hash(hash_str)
    assert retrieved_hash.decode() == hash_for_store_in_db




'''
    CREATE TABLE public.test_hash (
        hash varchar NOT NULL,
        create_ts timestamp not NULL,
        expiry_ts timestamp NULL,	
        usage_limit int8 NOT NULL,
        usage_remaining int8 not null,
        user_id int8 NULL,
        module_id int8 NULL,
        parameters_json jsonb null,
        is_deleted boolean null,
        CONSTRAINT test_hash_primary_key PRIMARY KEY (hash)
    )
    WITH (
        OIDS=FALSE
    ) ;
    CREATE INDEX ix_hash ON public.test_hash USING btree (hash) ;
    CREATE INDEX ix_create_ts ON public.test_hash USING btree (create_ts) ;
    CREATE INDEX expiry_ts ON public.test_hash USING btree (expiry_ts) ;
    CREATE INDEX user_id ON public.test_hash USING btree (user_id) ;
    CREATE INDEX module_id ON public.test_hash USING btree (module_id) ;
    CREATE INDEX usage_remaining ON public.test_hash USING btree (usage_remaining) ;
    CREATE INDEX is_deleted ON public.test_hash USING btree (is_deleted) ;
'''
