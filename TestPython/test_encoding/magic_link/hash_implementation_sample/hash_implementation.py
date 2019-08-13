import abc
import binascii
import hashlib
import json
import os
import datetime
from urllib import parse

from redis import Redis

from interactive_secure_links.python.hash.hash_implementation_sample.app import db
from interactive_secure_links.python.hash.hash_implementation_sample.models import InteractiveSecureLinkHash, \
    InteractiveSecureLinkHashAccessLog, InteractiveSecureLinkHashTotalAccess


_redis = Redis(
    host='10.0.0.2',
    port=6379,
    db=0,
    decode_responses=True
)


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


def create_hash(user_id, module_id='module_1', usage_limit=0, parameters_json=None):
    plain_text = f'{module_id}{user_id}'

    hasher = Hash(SHA512)
    generated_hash_for_link = hasher.hash(plain_text)

    hash_for_store_in_db, salt = hasher.hash_with_salt(generated_hash_for_link.decode('ascii'))
    hash_str = prepare_hash_for_link(generated_hash_for_link, salt)

    hash_for_store_in_db = hash_for_store_in_db.decode()
    hash_obj = InteractiveSecureLinkHash(
        hash_for_store_in_db,
        expiry_ts=datetime.datetime.utcnow() + datetime.timedelta(days=100),
        user_id=user_id,
        module_id=module_id,
        parameters_json=parameters_json,
        usage_limit=usage_limit
    )
    db.session.add(hash_obj)
    db.session.commit()
    return hash_str, hash_obj


def create_hash_log(hash_):
    hash_access_log = InteractiveSecureLinkHashAccessLog(hash_)
    db.session.add(hash_access_log)
    db.session.commit()


# fixme
def create_hash_total_access(hash_, usage_count):
    hash_total_access = InteractiveSecureLinkHashTotalAccess(hash_, usage_count)
    db.session.add(hash_total_access)
    db.session.commit()


def update_hash_total_access(hash_, usage_count):
    hash = InteractiveSecureLinkHashTotalAccess.query.get(hash_)
    if hash is not None:
        hash.usage_count = usage_count
    else:
        hash_total_access = InteractiveSecureLinkHashTotalAccess(hash_, usage_count)
        db.session.add(hash_total_access)
    db.session.commit()


def get_hash_from_cash(hash_):
    return _redis.hgetall(hash_)


def get_hash_from_link_hash(hash_with_salt):
    parse.unquote(hash_with_salt)
    salt = hash_with_salt[:64]
    hash = hash_with_salt[64:]
    hasher = Hash(SHA512)
    new_hash = hasher.hash(hash, salt.encode('ascii'))
    return new_hash


def prepare_hash_for_link(hash, salt):
    return parse.quote((salt + hash).decode('ascii'))


def init_hash_cache():
    hash_count = InteractiveSecureLinkHash.query.count()
    pages = hash_count / 1000

    hashes = InteractiveSecureLinkHash.query.limit(1000).order_by(InteractiveSecureLinkHash.hash.asc()).all()

    for hash in hashes:
        _redis.hset(hash.hash, {
            'create_ts': str(hash.create_ts),
            'expiry_ts': str(hash.expiry_ts),
            'usage_limit': hash.usage_limit,
            'user_id': hash.user_id,
            'module_id': hash.module_id,
            'parameters_json': json.dump(hash.parameters_json)
        })
