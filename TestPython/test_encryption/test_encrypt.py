import abc
import base64
import binascii
import hashlib
import sys
from datetime import datetime, timedelta
from urllib import parse

sys.path.append('/home/newshub/repositories/TestProjects')

from Crypto import Random, PublicKey
from Crypto.Cipher import AES
from TestPython.test_encryption.payload_pb2 import payload, param


AES128_KEY = b'Sixteen byte key'
AES256_KEY = b'Sixteen byte keySixteen byte key'


## profiling:
# pip install pyprof2calltree
# sudo apt-get install kcachegrind
# python -m cProfile -o myscript.cprof test_encrypt.py
# pyprof2calltree -k -i myscript.cprof


## Setup protobuf compiler
# pip install grpcio-tools
# alias protoc='python3 -m grpc_tools.protoc'
# for compiling a protobuf message:
# cd to/.proto/folder
# protoc --proto_path=./ --python_out=./ content.proto


class Cryptography:
    salt_length = 512
    iterations = 1000
    key_length = 32
    checksum_length = 64

    def __init__(self, algorithm):
        self.algorithm = algorithm()
        self.result = None
        self.salt = Random.new().read(self.salt_length)
        self.key = None
        self.checksum = None
        self.iv_length = algorithm.iv_length

    def _set_key(self, key):
        self.key = hashlib.pbkdf2_hmac(
            hash_name='sha512',
            password=key,
            salt=self.salt,
            iterations=self.iterations,
            dklen=self.key_length
        )

    def _set_checksum(self):
        self.checksum = hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=self.result,
            salt=self.key,
            iterations=1,
            dklen=self.checksum_length
        )

    def encrypt(self, key, value):
        self._set_key(key)
        self.result, self.iv = self.algorithm.encrypt(self.key, value)
        self._set_checksum()
        # print('iv:',  self.iv)
        # print('salt:',  self.salt)
        # print('result:',  self.result)
        # print('key:',  self.key)
        # print('checksum len:',  len(self.checksum))
        # print('checksum:',  self.checksum)
        return binascii.hexlify(self.iv) \
               + binascii.hexlify(self.checksum) \
               + binascii.hexlify(self.salt) \
               + binascii.hexlify(self.result)

    def decrypt(self, key, encrypted_value):
        value = encrypted_value
        self.iv = value[:self.iv_length]
        checksum = value[self.iv_length:self.iv_length + self.checksum_length]
        self.salt = value[self.iv_length + self.checksum_length:][:self.salt_length]
        self.result = value[self.iv_length + self.checksum_length + self.salt_length:]
        self._set_key(key)
        self._set_checksum()
        # print('iv:',  self.iv)
        # print('salt:',  self.salt)
        # print('result:',  self.result)
        # print('key:',  self.key)
        # print('checksum ex len:',  len(checksum))
        # print('extracted checksum:',  checksum)
        # print('checksum len:',  len(self.checksum))
        # print('computed checksum:',  self.checksum)

        if checksum == self.checksum:
            return self.algorithm.decrypt(self.key, self.result, self.iv)
        return None


class EncryptionAlgorithm(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def encrypt(self, key, value):
        pass

    @abc.abstractmethod
    def decrypt(self, key, encrypted_value, salt):
        pass


# https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html
class AES256(EncryptionAlgorithm):
    iv_length = AES.block_size

    def encrypt(self, key, value):
        iv = Random.new().read(self.iv_length)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return cipher.encrypt(value), iv

    def decrypt(self, key, encrypted_value, iv):
        cipher = AES.new(key, AES.MODE_CFB, iv)
        return cipher.decrypt(encrypted_value)


class LinkCryptography:
    encryption_version = '1.1'
    encryption_version_length_byte = 8

    encryption_packed_id = None
    encrypted_packet_id_length_byte = 64

    module_id = None
    module_id_length_byte = 64

    payload_version = None
    payload_version_length_byte = 8

    expiry = None
    expiry_length_byte = 16

    def __init__(self):
        self.key = AES256_KEY
        self.cipher = Cryptography(AES256)

    def get_link(self, module_id, payload_version, expiry, serialized_data):
        self.encryption_packed_id = 6412999854129152066
        self.module_id = module_id
        self.payload_version = payload_version
        self.expiry = expiry
        self.serialized_data = serialized_data

        self.payload = bytes(
            to_fixed_len_bytes(self.module_id, self.module_id_length_byte) \
            + to_fixed_len_bytes(payload_version, self.payload_version_length_byte) \
            + to_fixed_len_bytes(expiry, self.expiry_length_byte) \
            + serialized_data
        )
        self.encrypted_payload = self.cipher.encrypt(self.key, self.payload)
        return base64.b64encode(
            binascii.hexlify(to_fixed_len_bytes(self.encryption_version, self.encryption_version_length_byte))
            + binascii.hexlify(to_fixed_len_bytes(self.encryption_packed_id, self.encrypted_packet_id_length_byte)) + \
            self.encrypted_payload)

    def get_link_decrypted_data(self, link):
        link_byte_array = binascii.unhexlify(base64.b64decode(link))
        self.encryption_version = link_byte_array[:self.encryption_version_length_byte].replace(b'\0', b'').decode()
        link_byte_array = link_byte_array[self.encryption_version_length_byte:]

        self.encryption_packet_id = link_byte_array[:self.encrypted_packet_id_length_byte].replace(b'\0', b'').decode()
        self.encrypted_payload = link_byte_array[self.encrypted_packet_id_length_byte:]

        data = self.cipher.decrypt(self.key, self.encrypted_payload)

        self.module_id = data[:self.module_id_length_byte].replace(b'\0', b'').decode()
        data = data[self.module_id_length_byte:]

        self.payload_version = data[:self.payload_version_length_byte].replace(b'\0', b'').decode()
        data = data[self.payload_version_length_byte:]

        self.expiry = data[:self.expiry_length_byte].replace(b'\0', b'').decode()
        self.serialized_data = data[self.expiry_length_byte:]
        return self.serialized_data


def to_fixed_len_bytes(data, length):
    bytes_data = data
    if not isinstance(data, bytes):
        bytes_data = bytes(str(data).encode())
    to_append_len = length - len(bytes_data)
    if to_append_len > 0:
        return bytearray(to_append_len) + bytes_data
    elif to_append_len < 0:
        raise Exception(f'Greater than len: {length}')
    return bytes_data


class Profiler:
    def __init__(self, name, print_=False, logger=None):
        self.print_ = print_
        self.logger = logger
        self.exec_count = {}
        self.durations = {}
        self.clocks = {}
        self.stack = []
        self.push(name)

    def push(self, name):
        self.stack.append(name)
        self.clocks[name] = datetime.now()
        if name not in self.durations:
            self.durations[name] = timedelta(0)
            self.exec_count[name] = 0
        self.exec_count[name] += 1

    def pop(self):
        name = self.stack.pop()
        self.durations[name] += datetime.now() - self.clocks[name]

    def flush(self):
        while len(self.stack) > 0:
            self.pop()

        if self.print_ or self.logger:
            self.dump()

    def dump(self):
        for title, count in self.exec_count.items():
            duration = self.durations[title]
            text = f'{title}: {duration/count} ({count} executions, {duration} total)'
            if self.print_:
                print(text)
            if self.logger:
                self.logger.info(text)


def init_data(params):
    x = payload()
    x.params.extend(params)
    x.type = "unsubscribe_inbox_report_membership"
    x.token = "vCHDYq1RcFaj8ynfuRyxDaEJfsa6Vw"
    user = x.user
    user.id = 6413005516439552837
    user.name = "user1 familiar"
    user.activation_status = "active"
    domain = x.domain
    domain.id = 6413005516439552831
    domain.name = "domain1"
    return x


if __name__ == "__main__":
    start = datetime.utcnow()
    # os.environ['TERM'] = 'screen'
    # subprocess.run(["watch", "-n", "0.1", "free", "-m"])
    # os.system('while true; do (echo "%CPU %MEM ARGS $(date)" && ps -e -o pcpu,pmem,args --sort=pcpu | cut -d" " -f1-5 | tail) >> ps.log; sleep 0.001; done')

    import os
    pid = os.getpid()
    print(pid)
    # command = f'PID={pid} ; while (kill -0 $PID > /dev/null 2>&1); do (echo  && ps -p $PID -e -o pcpu,pmem | cut -d" " -f1-5 | tail -n 1) >> ps.log; sleep 0.01; done'
    # os.spawnl(os.P_NOWAIT, command)
    # import pdb; pdb.set_trace()

    profiler = Profiler('encryption', print_=True)
    link_crypto = LinkCryptography()
    module_id = 'unsubscribe_daily_report'
    payload_version = '1.1'
    expiry = 1528629954

    print('\n\n ************************* \n')

    x = init_data([
        param(id=6413005516439552834, name="test1"),
        param(id=6413005516439552830, name="test1"),
        param(id=6413005516439552835, name="test1")
    ])
    data = x.SerializeToString()

    profiler.push('create one encryption with 3 params')
    link = link_crypto.get_link(module_id, payload_version, expiry, data)
    print("len: ", len(link))
    print("link: ", link)
    link_str = parse.quote_from_bytes(link)

    profiler.flush()
    print(len(link_str))
    print(link_str)
    unquote = parse.unquote_to_bytes(link_str)
    assert link == unquote
    profiler.flush()
    #
    print('\n\n ************************* \n')
    # link = b'MDAwMDAwMDAwMDMxMmUzMTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDM2MzQzMTMyMzkzOTM5MzgzNTM0MzEzMjM5MzEzNTMyMzAzNjM2ZDQ0MWM3OGI5NjcyNjdmZWRiNjJmZjc1M2MxOWE1N2I1OGFmNTU0MGY2MmYyNjljMjIyYzY4NDFiOGM3Mjk2MGYwMzFjM2U4NGU4NWFhYzVjNzUzMjY0MmU1NWZkYmYyOWYwZTBkNWNlY2RkNzVhNmQxZDVmYzM5MjM3NmQ3YjBhNjQ4ZTcxOTU5M2MyMWNmM2RmMGY3YjMzZGY3YjQ1ZWU3MmRiMGViOThhZmU2MGZhMjk3ZDk5YThlNTRmNTI5ZDY1OTNiMzRiZWU1NjJiNjI3MzU2MDllYTY5YjA4OWJhODE3ZmUzZGQzODBhYTQwNGE5ZTVlM2U2ZGE1ODhhNzhkOTJlYzY2YzIzZTQ5MDgzZGUxNDE5ZGNlNWU3OGEwODcxZGFhOWIxYmU3NzQ3ZWY3YzNkYzA3Nzk3ZWQxMTNjZjAwMDBlY2UzMGZkNzczY2EwYWU5NDNjOTgzM2QyZTI0MWFhYmZjZjMyMWNiZDUxZTY0ZmI4MmVmYzE2ODcyZThiNDljYzVmOTcyOTM4ODY1OWY1MTQ5NTVkYWI1MDI3MTQ1MGI0YTM1NDhkZjJlY2E5YTZiZWU0OTUxYjhmNTRiZTY3YWJjYjNjZTBiNzdhNmMxZmFkMWQ3Mzg5OTc1NjVjZGI2YmZhYjkxMTczZTZlMzgwNzg5ZTZiMDBmZmI4NjhlMzllNmJhYjAwMjI2MjAwNTNlN2ZhODJiOGMwNjYwZGQyYjNiNmZjMTUyMGM1NDU4YmUzYjc3Yjg3NjgyYWNhMjRiNTc2YWRlMmY0MzE4MDAyNTZmNjcwYWJkMTIxNjRiYzFkNDU0NThiNTViNjU5YzgxZmVkZDA2ZmY3MGI1OTIwY2ZmZTNkYzBmYTNkYzI5MGU1ZTBhOGNlMWNjYTUyOTJjOGIwYmRkNzIwNmJiNTVkYjZmNTM2ZmNkYzhiNjQzZjlhMDk4ZjU0Mzk0NjA3ZGY4YzgzODg2MjU1NWI5ZDBjNWVjMjlhYmEyYjk1NWIwNzM3YTlmOWUzZDNkYzEzOGU2NjRhNTc1MmY3YzEzZGZkNzJmNjM4NThlYTRjMGVkM2YxZDg4NzQ1NDUxYTNlNzAyN2Y2OGEzZTIwMmYyMDQ1MjkyYzcyODY5Y2Y2YmNmZGRkMDU4MWYwNWE2NmI5NzUzMDE2NjA2OWJhMjVlNDY5NjNlYzU1YjJmMTZkNDliYzVlNWVmMTk0MjJmZGY5MGUwNWU5YWEzMzc5YjJhOGJhNGJlOGM4NTVhMDRlZmJjNzMzM2VkMzlkMWZjZTI1MWQ2ODg1NTNmODA5NGUyMTAzMWNiNDI0OGM0YjUxMGU0NDFiYzFmNmYwYzVhZWRkMGE4NTE1ZDZmNDE1YmQ5OTM2OTBlY2QzMzU5N2UwMGY5NWZjNDJjOGFkOGM3N2Y3MTNlOGIzY2I1NTQ4ZjY5OTI1NTAyOGY2MDY5MTc2MGIwOTQ3YmZhYzE0N2E4NTg3YzBhZjNhNjlhYzA2NWQxNGMwM2VlZjNlMGM2YTFlMzk5MWE1ZDdlNTZlYzYyZDZiMmViODYwNWNmYTBlODBhMjAzMDFlZjg4ZGMxMTljYTkxZGRlZWI2NDc0ZmIyY2VjNTUyOTkyZWYyNjYwMDVhNTRjMzFlNGI4MGJjYzU0OTgxN2M1MTQ3NWQ1ZWExM2ZjM2I5YzEwMGZiOWNkOGZiYWI1YzViNWE3NzZmYjAwMjg5OGZkNmU4MGIwNzAwMGFhZDY1M2IyMWI2YjhmNTk3ODhmZjJiMzI2NjIyMGI1NzNiMjQyZjc3ZGUxY2RkYmZlNzFhOTRiMzk4ZDRjNDc4MGVkODE2MTEzZjQzNGRhNzE4MTMwM2IwYzA0OTA5MGU2ODI5ZjM2NGE3Yjg2ZGEyY2RjZjhlM2RkZjRjNTNiYzVjNzExYjU0M2M0MjNhMGMzOGM2ZjNjZmE1MTYxZGEyYzM4MjI2NDFkOGQ2Zjg0OTM2YmE2NmVmZjdmZTYzMmQyZmUxMGRmNDU2M2M1ZWQ3ZTIxZTk3ZWQ0ZDlhYzVjY2NkOWVmN2Q1MDg4NTNhYzViNWI5OWVjMWZkNTRkZDNiMGU4MGI5YjJlZWQ0NmY0ODg2MDZiYmM1NmY2YzM3NThkZWZjYWM2NWI4Yjc4M2U3MjM0MGI3Njk3YjhjZTc3Mjk0ZDk4OTIwNTZkOGE2NmIxNWYxNTA5YTJlZjBhMjY2Yjg2ZmNiMmIwYTAwMzYwNDhmMmY1OWFlN2E1MTg0YzZjMGQyMWQ4Y2M0MDgyNGRlNzI4ZDdlOThhYjE0MDA5ZWUyYWZiOWVlMjc3MA=='
    # link = b'MDAwMDAwMDAwMDMxMmUzMTAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDM2MzQzMTMyMzkzOTM5MzgzNTM0MzEzMjM5MzEzNTMyMzAzNjM2NTlkZTM2NDM2Mzg5NGNlMmZkNmFmYWJkZmUwNzc4YTgzMGQxODViZDM0ZjZhMmNjZjhmZTNjYmMwNDlkMTE1NDM1MGViNmJiOTg1YTlmMDU3MzAwN2MwNDc5NGZhN2VhNTk2NzdkZmMwMDgyZWUyZjQ5YTYzYjQwMmFiMGZlMWQ2ZDcyNTJkNDIwZTI5MDU2ZjE4OGIyYzU1OTZkYzkwZWFhYTBmMWU3MmM1ZmIwNjhhZmNiYmNmZjM1NzIzNzA3MDg1YjU3ZjY5MGYzYzE3NGY3NDRhOGE1ZmExZDFkYTNjMTJmMzdiOWFkZDg1MTc2YTc2OWRhZWVmMjllMDY1YjdmZDk2N2ExZDY5ZDE1NjM3YmU4ZjZjNmQ0NWVkZWIxYmQ5M2MxYmQzN2Y3OWFkZDFjZDgzMDAzNTJkODM1MzBmY2Y3OWQwYjVjNGQzM2EwMGQyOGY0MDQ0ZDI5ZTRhM2RkMWY5YTYzOGNlZjM4NzJmZDE0MTFhNGYxNzEwM2VjOTM5MjhkNDVhMmZiYTU2Y2MwNTViMDBlMWZmYWFhMzBlOWY2NTcwOGVkZmJhNzA5ZWRiZDA4MmQ4MmE3ZmZmZjUyNDNkMTQ3Yzk5NDdjMWViM2JmNDM1MDQxMjczY2U1MjlhZjg0ZTAzZWU1NGZmY2Y2YjI1Y2Q5ODk5MTRiMTFkZDlhMjU1NTcyMDFjMmIwZTVlNjEyMzgzNDNlM2NmY2YxMzlmNDIxOWJhMGEwOWI0OTZiZDYzNjE4NGJiMjljZDMwMzBhMjgxNzY3YTgzNzJjOGY2YjNjZWU1MzQwODljN2NjMWJkZGE5NDY0MDQwMWVkZDhkYTRhNzc2ZjkwZGJjMWY2ODZiMmEyZTQzNzgwNTk2ODA3NmI0MzljYWRmZGY2OWUwMWMxYmRkMGJiOTdmMzhkYzA3MDMwNDYyOTBiNjVmNmFhZGQ4ZTNlZTc4OGNjM2QyY2I4MzhjZDBlYzg1OGMzOGYyZmZjMTBkNmEwY2JjODhlODU4NmVjYjJiNzk0YzM4ZGY0MDViODE4Yzc4YzJmZGU0ZWVhYWViZDE2ODlmNTA4MGVmNDYxZGQxOGIzYWExYTMwM2ZlMDdkM2VlMjI4MjNjNTg5NDg1ZTIyYjA3NDM2MDU4OTBhY2IxZDljMTk5YTRkNWQ4YjUzYzlmZjk5YWU1NzNhY2YzYzBjNmU3ODUwODJkNDVkNDY3OGVhMzQ4ZWRhM2FmOWJiODZhODliMGUwM2Q4ZTA5YTlkNTU5NjVmYmNiMTQ5YmM3NTE3ZDc2MTZlZTlhOGNlMzk3ODZiMTEwNDMyNmUxYzc3ZWUyZGYxMDNjYmIyYzg4NTBiNTk0ZTViNzAwYjU3ZjYwYTczZjNlNjNjZGI2MTY5NzQxNGU1Nzg1NTVlZmNmZmM4MmM1NmZmNThjNGUwMThmZWRhZWE3MDdiMDVkOGE1MDUyNDA5NjdlZmFjZWViZDRjZWRkOGU3YThmYTEyNWE0OGUyM2E5ODQ3MmIzMzAzMGQ0MzNlNzcyZWFlMTU1YTNhYTUxNGFhODZhZTAzNDQ2ODdjM2U3ZDQ4MGFkZDIzNTIwZDZkMzYyMmU1NDYxMjYxNmJiODMwYTQyZWU5NTI3NzFiYmU0OTY1YjNkNWFiMjc2MzIwNDZiN2QzOWQ1ODQ4YWNmOWViYzA0ZDBjNGU2ZWE1NWQ0NjgyMDUxZTI5ZWQ1NDM1MmRhY2QwZjA1OTk0Yzk0NmM3MzY4YWUzMzAyNTA2MjdiOTI3ODMwY2E0OTJkZWIyYmVmMzZlNDJkN2FjZmJkZDViODM5YTIxZWI0ODJiNmE3ZGUyYmE5YjNlYjQ5MDEyNmNlYTFjNDY4M2M5MzYwNGYzMzE1NjAwNzFlYjNmZDg0NTgyM2NkMjZjMmFjODE5YjVjOTJiNWE3YzEyNTY1MzdiZDJmN2Y4ZjAxMjQ4NzU5ZDQ3OTE1Yzc3ZmI2NzU1MDk0ZTEzMTA0ZWJlOTQ0MTYzMjAwNGRkMDk0YmYxNzM3NTg5NDc2MjE5NzkxOGFmNTAwZTI1MzBiZDdhYzAxMjUwMDRmNDc3ODFjOGEyZGU1NzAyZGRjN2QwNzU2ZDQ5OGFiMTE4MTQ0MWNjMDQwYmJlZjU0N2U4ZWE3MTE5MWMwZDNmNjBjMDZlNGRkNzRmZDg2Mjg3NjYzMWU4ODFjMGEyZDBkYmYwYTQ4MDU2YTE0OWQ4MjBmMmY3ZWQxYzRlMmNhMTAxMmYwMTUxZDA0ZDEzMWIyY2VjYTljMjdlZmJiZTM5MDE2NzMxMmQxMTQ4Zjk1YTMyN2NlMzQ2NTY1ZWU2M2UyZDBmNTQzZjQ2MWI3Y2RhNmFhOTZjN2FmOGFhYzRlODBkNTQ4MzdiZGE4NTU5YzI0MmNiYzBkNGY3MzM4ZTgxNTE2NzEwOTVlMjI2NWY3ZGYyNmZlYzYyYjIwZDYxMmUxOWYxMTdhOGFhMzAwZjdkY2RjMDRjNTc1N2ZlN2MzNGEzMDk3ZWFiZmNjYmM5OGZiNzc3NDJjZWVhMmI3YzczODg0YzVhYmViN2ZiNTk1M2EzOGNiZWYzM2U5ZGJiMmRkNDI0ZGU0MzJkNDMxYzA2ZjgxMmY3OGRmNGMwYzQyM2U2OGE2NmM3MzE4ZTUyMjE0OTg0NWY4N2Y5ZDE1Mjk4ZDVhNGM2NDBjOGNlZTFhMDI0OWQ3N2VkMWViOGQ4ZGUxODdhOWRhNDVjYTM3Njg0MzRiNzIyMDU5ZjcxZThkMmEzNTYwYzllMzM5ZDdhOWE5NWZmZmQ2MjkwMzJjZTJkY2Q5Y2JmZDRmYTI4NmU1NTU3MjIwZGNlNDk1ZTY4MGRiYWYzM2E2ZWZhZmQ4N2I1ZGI2MTQ3MTRlOTMwYjM1ZmFmNjJmZWFhZmQ1YTExMDY0YzgwMDk0YmU4ZmY4NzMzNGIyMjBiMDZjNGZiMDhjYTkwYTE5ZTQzMGVkYmIyOWVjZDhlNTIxMGRjM2Y2ZThhM2JhOGQyNDIzODkxNDkxOTQ5NDkyMGUzYTNhZjljYjI3M2I0ZjlkNjYwNWE3YWIwNWU2NWI2YTUxMjIwMzg3NTllNjIwYmJkNjY0ZTA3OTk3YmVkYjc0NDA3ZTNmZTM5Y2JiMGVkMjczZmQwYWJhMjE0YmU3YWUxNTdlOGYzM2ZiODNhYjExZjMzY2I5NzBmZjM1Y2UxNzczYTNhMzBkM2RhYWViNjBlNGY4NTYxOTdhZTI0N2RkZDhiMDYxZjFkYjg1NWM0ZTllMTg0MmM0MDRmN2YxOTc1OTkxOWJiNGQ1ZmRmNDg3MjBiOGE3NWIyM2Q1ZGIzNzYzZmQxMjgwMmY2M2E4MGU2MjUxYTJkMGY5NjQ1NGMwZjU5MDUzZWExMGQ1ZjQzODJiNDI3YWM1MTZkNzU1NmUzN2NmYmRlZmM4MTNiODZjZTBlZmMwMzMwMzIzYjllY2FlMGJmM2I5MDcwNzQ5ZDcyYjkxNzk2YTIyZmQ2OWJhM2EwOWQ4NDM4YjhjZjBjMzk2OTBhYjM5N2EwZTJkZDAzZjExOTVjZmY2OTM0Yjg0NGEzMjJiODI2YjkyMDRiYzYyZjMwNTc2NDk0NWRlMDMwMGZlZjA4Y2JkYzA3YzgwOTAzMDA4MTZiY2ZlYjQ0YTFhOGU2YjZlMzM4ZGYwNDA4NDVkYjBiMmEyY2MxMTVhOWMzMTY3NGVhYjRiODg1MTMzZDI5Y2FiZWFiYjkwOTQ4YzJmZDBmYTczMTY0MDQ3ZGU3ZTU1MjdiNTE4MTA3ZmUxOTUwMDMzYzY2Yzc5ODQzYmE3ZDNkOWVlZGU3OTczMzM2MGI2MWQ0MzYyM2RlNTU2MjAxZGUwYmI0NWNmNzcwOWZkMzQ4MDQzMWE0NTQ3NDRiZGI4NGU4N2YyNzQzODBhMGZkNDVmYTkxMmE5M2M1NGYyOTA5MjcwMjc2MTY5YmYzOWNlMmQ3NjlkOTFmZDU1ZWIwYjQ2ZWE0OGVjYjQzZTRkYWRkOTYyNjQ1MTE3OTY0MTc0YThkMGFjMjA1Mjc3ZWI2M2Q5MmU0MzcxZGZmOTNlYjI1NTcxN2Q1ZjhlNTU3OTRiZjU1ZWI4YzcwMWQxNjVlNmE1Y2E3M2YyMmNmMjExOWYzZTM5YWY4YzRhMzU5MWZhZDBmMDcyOTE0ZGVhNmQ4NzNiM2ZlOWNmMjc5OTlmODU1NGQ0ZmRiZGRhNTc1MjY3ZmY4MDJhZDg5ZDNiNDZkOWIwZTJhYTZmNWU1NDgxMzhkYzgyMzUzMTc0YWUyMzM4Y2E3MDIxMzFjMjFlNjVlMjVjZjgxNzdlYzVjZGVkNWVkZTI3ZmMwZGFiYjIwNTg4Njc5OGQzOGVmOTBkMWI4ZmE4YzU1ZGU2MjAyNzg3ZTE1MGNkNGI4NzZiMWM4YTdiMWZkY2NjMzEyODE4NTk4MjM0ZGRkZmM0MzlmMDM4NDRiYmE4MjFlM2YxMDdjMGRmNDc3ZDE4ZDIzNTU0NWMzODZiOTM0ODI0MjA0MGNlNjU1Nzc3MGRiMTVkNmZiY2U5MzczZWQzMDgwMTFjMzMyNGJlYWQ5YWY0ZWJhNDdkNzE2YmRkYTFhN2E2ODYxYjRkNTg3NWQ3YTg3NGUzYTc0ZGM5Njk1OWU5ZmNhMzcyOTY3YzgzMzRkNzQ4OTA5OTAwYzVhZDI4NDVkYmEzMDA2OGJlYWY4YTljMGMyZjA3MjNiMDNkOWUxODk2Yzc2Y2Y4ZjA5NTBjNWFmM2Y4ZWJjZjRhMTVhNWViYjA3NTNlODM3MGE2YTI3MjlmZDQ3YTEwZDIwYTc2ZGE0YTZjZDAzZDJjZGEyYzQ5NTA0ZDE0NzM0ZDc0NGY0YjBjZjNjMGM1NmFlZDY0YmQ0ZThlYmUzN2ZhNTFhMzA4OGM1M2ExZmM1OWRiMmRlNTRmYzI3YzAyZTQ0NDc5Mzg2NzczNGQ2MmE5NjdiZWQ4MjhmMzg1YTEzOWQwZTlmMGEwYWRkNjFjNGZkNDc5NjYwYWNiZDMwNjg2Mjk1NTEzMWZmZTdhZWJlMDc5YjI2M2M5NDhlOTY3MWMxZmIxYjY1ZjY0YmU3MTUyYzdmZjE3ZDhjYzE2ODI3ZWYxOWJlNWU1ZjkyOTRjYjNkNjE2ZTY0YTE3Yjc1YmY2ZmY1ZDFkNmU4ZTkxODI3ZThhZjdjZTQ3YjE0MjYwMjcwNmM2MmIwN2U2YWVkZDFiZTg1OTUwNWI1MWNiMjlmOTI2ZDM2M2Q4N2JkY2NjN2E5ZWEyNmRlYjUwNTliOWNhMzViNDA5ZmM0ZTU5YmY4YTg4MDFjNTgxNWZmZDcwZTkwOTUxOGVjNWE1NWI2ZmM0MTllOWYxOTg0MjJmOWY1YWY5MjVmNThjYTkxZGI5MTc2NTg4NTIwOTYwZDEyMWQ3OGVlNWQ0NDBiNzIzMGJmOTNkYjQ4YWIxOWVkNjMxNmRjOTZlZTgwOTk3Y2UyYzliNDI2MTE1Y2M1NDc0Y2RkYzYzMGExYjY5MjA4MTM0YTdmOTE3M2YwOTkzMjRjYTRmZjQzNTZjYjk3NWNiMjM4MGE3M2ExNzgxYzI2NTRhNjFmOWM3OWM0MmVlOWEwNmYyNThmYzUwNjYyNzU4ZmQ1YmYwY2Y4NjhjMmVmNTY1NmI2YWY5YjhhYTIzMjNmN2EwMzc2ZTgzNDM0MDE3YjM5OTRmYzk0MTQyNTg1NWQ2YzcxYWM3MTFiMzJkYWI5ZDRiZjRhZjc1Njk1ODliMmZjNDFlZDgxMWJlYTU2MTM2ODNiMTA2ZGM1YWRmOWUzODE2NGY0ZDA1ZDIxODYzZjIwODRlNjU0YWUwZTA0MTc0ZDQwZGVlMjUyNzJkOTQyMmY2ZGVkYTVjNTFiNGIyMDdkNjAzZWZjOGUzZGIyZDAzYjZlOWY5MzYyMWE4YmZhNzc3ZTQyNGU1YzBiYmIyNzhmMWNkZjI1ZmI3OGIyNzUxYjBiMDdkZTM1NGVkMjg1Y2E1MGQ4ZjAyMTRjMDA1NjU1MTI0YzU5YTMwOWQyZTgxZDk3NjE3M2VlMWI0NGQxYmVhY2FkZDU0NjAxMDU4ZTNlM2M4ZGIyY2NkZTU5NTJkYzgzMzMyZTMzOTg0MzAyNjU3NTlmNTU4YjM5YThiYzM4ZDg3MGFiYTUzNGRkOTk0MzQwNzU5YjQzZDA3MTZhODQwYjgyMDk2NDFkNjM1NTU2ZTU2NzVlYjYzNDY1MGIzZGE3OWE5OGMxYzNkYjZhYzRjMzg3ZmQ0ZjU2M2IwMjA5NTA3Nzk1ZDFhODc3ZDhkY2QyZTcwYjAyMzc2MDVjMGRkN2Q1ZWI5OWUxMjMyYmZjMjU5OWJlZDg2NWUzYmMzNjc0MjM0Y2MyYjY4YjBjZTU1NjFkM2E3YWE2Yzk3MmU1ZDJhYmRhYjE2OGQ1OGJkM2ZiNjJkODM2ZWY1ZDJjMzc0NWViOTYxMWVkZDI2OTBiMjE1Mzk2Zjk4NjQzZGE1MjQxNTYxMmM3ZGY2ZTczNzA5MWIyZDFhMzhmNzUyOTI5NWE3OTc3MDQ5MGM4YTU1NDVjNzc3ODU5OWJmNGU3OThkNzU1MGJlMzExYTA3OGE2YWQ2ODY2OGZhZmU2MmQyMjY0MGQ4MzRlYmU5YTNjNGYxNjA3ZTU4ZjFlMzRjYTk3OWFkMzg2NTVhMzQxOWI2YWY1YzIzYTBkZTI5NGRjMzUxMmRkYWYxNjY0MmQyNzdiZTc0MDQ2ZDliM2Y1OTI1OGJlMDFmNWQxNzE2YWMwYjUwMzU3MTg0MTVjNjE1YTJlNjExMzRlMDY5YmYzZGNmOWQwZWJkZGI2MTI0ODM0ODE2NzA5MTczMzhmYjIwOTdmMzFmODg0ZDI2ZGFjNTgxNDUyMDdiZjk4MTA0MmZlZjQ4NDllNzIzYzBjODgwZmMwY2Q0Y2Y2ZmQ2YTYyYWEzZGZkMGVkMmRkZWNhMTI1NjAwODA3ZA=='

    # for i in range(1):
    #     profiler.push('decrypt one encryption with 3 params')
    #     decrypted_data = link_crypto.get_link_decrypted_data(link)
    #     profiler.pop()
    # profiler.flush()

    #
    # print(psutil.cpu_percent())
    #

    # result = payload.FromString(decrypted_data)
    # assert result == x
    # assert module_id == link_crypto.module_id
    # assert payload_version == link_crypto.payload_version
    # assert str(expiry) == link_crypto.expiry
    #
    #
    # print('\n\n ************************* \n')

    new_data = payload()
    profiler.push('create 1 link with 100 params ')
    # for i in range(1, 97):
    #         new_data.params.extend([param(id=6413005516439552834, name=f"test{i}")])
    data = new_data.SerializeToString()
    link = link_crypto.get_link(module_id, payload_version, expiry, data)
    # print(link)
    print(len(link))
    link_str = parse.quote_from_bytes(link)

    profiler.flush()
    print(len(link_str))
    print(link_str)
    unquote = parse.unquote_to_bytes(link_str)
    assert link == unquote

    # profiler.push('create one link with 1000 params')
    # data = x.SerializeToString()
    # link = link_crypto.get_link(module_id, payload_version, expiry, data)
    # links.append(link)
    #
    # for i in range(len(links)):
    #     profiler.push('open 100 links with gradually increasing params from 1 to 100')
    #     link = links[i]
    #     decrypted_data = link_crypto.get_link_decrypted_data(link)
    #     result = payload.FromString(decrypted_data)
    # profiler.flush()
    #
    # profiler.push('open one link with 1000 params')
    # decrypted_data = link_crypto.get_link_decrypted_data(links[-1])
    # result = payload.FromString(decrypted_data)
    #
    # links = []
    # new_data = payload()
    # new_data.params.extend([
    #     param(id=6413001460547584194, name="test1"),
    #     param(id=6413001762537472258, name="test1"),
    #     param(id=6413002328768512322, name="test1"),
    #     param(id=6413002639147008386, name="test1"),
    #     param(id=6413002815307776450, name="test1"),
    #     param(id=6413002865639424514, name="test1"),
    #     param(id=6413002915971072578, name="test1"),
    #     param(id=6422682304249856258, name="test1"),
    #     param(id=6422682295861248066, name="test1"),
    #     param(id=6422682300055552130, name="test1"),
    #     param(id=6422682300055552194, name="test1"),
    #     param(id=6477492265156608130, name="test1"),
    #     param(id=6477492961411072194, name="test1"),
    #     param(id=6477492994965504258, name="test1"),
    #     param(id=6448592722067457282, name="test1"),
    #     param(id=6448536635834368322, name="test1"),
    #     param(id=6435457541865475778, name="test1"),
    #     param(id=6467286680469504066, name="test1"),
    #     param(id=6448647977828352130, name="test1"),
    #     param(id=6448537986400256450, name="test1")
    # ])
    # data = x.SerializeToString()
    # for i in range(1, 10000000):
    #     profiler.push('create 10000 links with 20 params')
    #     link = link_crypto.get_link(module_id, payload_version, expiry, data)
    #     links.append(link)
    #
    # for link in links:
    #     profiler.push('open 10000 links with 20 params')
    #     decrypted_data = link_crypto.get_link_decrypted_data(link)
    #     result = payload.FromString(decrypted_data)
    # profiler.flush()
    #
    end_time = datetime.utcnow() - start
    print("taken execution time: ", end_time)


#  check time
#  check ram and cpu usage
#  check request per second








