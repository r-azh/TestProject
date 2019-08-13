#!/usr/bin/env python
import base64
import hashlib

from Crypto import Random
from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-s[-1]]


class AESCipher:

    def __init__(self, key):
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]))


cipher = AESCipher('mysecretpassword')
encrypted = cipher.encrypt('Secret Message A')
decrypted = cipher.decrypt(encrypted)
print(encrypted)
print(decrypted)

#
# $cipher="AES-256-CBC";
#         $ivlen = openssl_cipher_iv_length($cipher);
#         $iv = openssl_random_pseudo_bytes($ivlen);
#         $salt = openssl_random_pseudo_bytes(256);
#         $iterations = 1000;
#         $key = hash_pbkdf2("sha512", $passphrase, $salt, $iterations, 64);
#         $ciphertext_raw = base64_encode(openssl_encrypt($content, $cipher, hex2bin($key), OPENSSL_RAW_DATA, $iv));
#
#         $hmac = hash_hmac('sha256', $ciphertext_raw, $key, $as_binary=true);
#         $result = base64_encode(bin2hex($iv).bin2hex($hmac).bin2hex($salt).$ciphertext_raw);


#       const ivlen = 32;
#       const sha2len = 64;
#       const saltlen = 512;
#       var c = atob(content);
#       var iv = c.substr(0, ivlen);
#       var hmac = c.substr(ivlen, sha2len);
#       var salt = c.substr(ivlen + sha2len, saltlen);
#       var encrypted = c.substr(ivlen + sha2len + saltlen);
#       iv = CryptoJS.enc.Hex.parse(iv);
#       salt = CryptoJS.enc.Hex.parse(salt);
#       var key = CryptoJS.PBKDF2(passphrase, salt, {
#         keySize: 256 / 32,
#         iterations: 1000,
#         hasher: CryptoJS.algo.SHA512
#       });
#
#       if (CryptoJS.HmacSHA256(encrypted, key.toString()).toString() ==
#         hmac) {
#         var decrypted = CryptoJS.AES.decrypt(
#           encrypted,
#           key, {
#             iv: iv,
#             mode: CryptoJS.mode.CBC,
#             padding: CryptoJS.pad.Pkcs7
#           }
#         );
#         decryptedContent = CryptoJS.enc.Utf8.stringify(decrypted);
