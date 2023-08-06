# -*- coding: utf-8 -*-
# @author: YuHuiMing
# @file: sha512_aes_256.py
# @time: 2021/7/29
# @desc:
import os
from base64 import b64decode, b64encode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decrypt_pbe_with_hmac_sha512_aes_256(decrypt_str: str, secret: str) -> str:
    # re-generate key from
    secret = secret.encode()
    encrypted_obj = b64decode(decrypt_str)
    salt = encrypted_obj[0:16]
    iv = encrypted_obj[16:32]
    cypher_text = encrypted_obj[32:]
    kdf = PBKDF2HMAC(hashes.SHA512(), 32, salt, 1000, backend=default_backend())
    key = kdf.derive(secret)

    # decrypt
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decrypt = cipher.decryptor()
    padded_text = decrypt.update(cypher_text) + decrypt.finalize()

    # remove padding
    un_pad = PKCS7(128).unpadder()
    clear_text = un_pad.update(padded_text) + un_pad.finalize()
    return clear_text.decode()


def encrypt_pbe_with_hmac_sha512_aes_256(encrypt_str: str, secret: str, salt: bytes = None, iv: bytes = None) -> str:
    # generate key
    secret = secret.encode()
    salt = salt or os.urandom(16)
    iv = iv or os.urandom(16)
    kdf = PBKDF2HMAC(hashes.SHA512(), 32, salt, 1000, backend=default_backend())
    key = kdf.derive(secret)

    # pad data
    pad = PKCS7(128).padder()
    data = pad.update(encrypt_str.encode()) + pad.finalize()

    # encrypt
    # cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cypher_text = encryptor.update(data) + encryptor.finalize()

    return b64encode(salt + iv + cypher_text).decode()


def parse_apollo_secret_jvm(apollo_secret_jvm: str):
    """
    parse apollo_secret_jvm: like -Djasypt.encryptor.password=KqiDYIroMUEVRBCW -Djasypt.encryptor.algorithm=PBEWITHHMACSHA512ANDAES_256 -Djasypt.encryptor.key-obtention-iterations=1000 -Djasypt.encryptor.provider-name=SunJCE -Djasypt.encryptor.salt-generator-classname=org.jasypt.salt.RandomSaltGenerator -Djasypt.encryptor.iv-generator-classname=org.jasypt.iv.RandomIvGenerator -Djasypt.encryptor.string-output-type=base64
    """
    secret_jvm_dict = dict()
    if not apollo_secret_jvm:
        return secret_jvm_dict
    for kv in apollo_secret_jvm.strip().split(" "):
        secret_jvm_dict[kv.split("=")[0].split(".")[-1].replace("-", "_")] = kv.split("=")[1]
    return secret_jvm_dict


if __name__ == '__main__':
    password = "hZ8ITKrmd7fn9tkH"
    encrypt_text = "2bC1BWPffYnN"
    encrypt_result = encrypt_pbe_with_hmac_sha512_aes_256(encrypt_text, password)
    print(encrypt_result)
    decrypt_text = "KT4lHOm1oGaulHnDKxLkxudYLjkKWPuk57/5M1+e863DOzu9APnkXJeRtafaLbq+"
    decrypt_result = decrypt_pbe_with_hmac_sha512_aes_256(decrypt_text, password)
    decrypt_result1 = decrypt_pbe_with_hmac_sha512_aes_256(encrypt_result, password)
    print(decrypt_result)
    print(decrypt_result1)
