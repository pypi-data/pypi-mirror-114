# -*- coding: utf-8 -*-
# Author: ZKH
# Date：2021/3/12
import os
import re
import time
import functools
from flask import request

from yqn_project_pro.utils.sha512_aes_256 import decrypt_pbe_with_hmac_sha512_aes_256, parse_apollo_secret_jvm


def parse_request_with(parser):
    def wrapper(view_func):
        @functools.wraps(view_func)
        def inner(*args, **kwargs):
            request.kwargs = parser.parse_args()
            return view_func(*args, **kwargs)

        return inner

    return wrapper


def time_it(timeout=None):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            caller = func(*args, **kwargs)
            waste = time.time() - start
            if timeout is None or (isinstance(timeout, (int, float)) and timeout < waste):
                print(func.__name__, 'waste time: %s sec' % waste)

            return caller

        return inner

    return wrapper


def decrypt_apollo(fun):
    @functools.wraps(fun)  # 为了保留被装饰函数的函数名和帮助文档信息
    def wrapper(*args, **kwargs):
        """这是一个wrapper函数"""
        apollo = args[0]
        apollo_value = fun(*args, **kwargs)
        if getattr(apollo, "apollo_secret", None):
            decrypt_secret = getattr(apollo, "apollo_secret")
        else:
            apollo_encrypt_jvm = os.environ.get('APOLLO_ENCRYPT_JVM', "")
            decrypt_secret = parse_apollo_secret_jvm(apollo_encrypt_jvm).get("password", "")
        if not apollo_value:
            return apollo_value
        spilt_val = re.match("ENC\((.*?)\)", apollo_value.strip())
        if decrypt_secret and spilt_val:
            val = decrypt_pbe_with_hmac_sha512_aes_256(spilt_val.group(1), decrypt_secret)
        else:
            val = apollo_value
        return val

    return wrapper


def decrypt_apollo_with_secret(secret=None):
    def inner(func):
        def wrapper(*args, **kwargs):
            apollo_value = func(*args, **kwargs)
            if not apollo_value:
                return apollo_value
            if secret:
                decrypt_secret = secret
            else:
                apollo_encrypt_jvm = os.environ.get('APOLLO_ENCRYPT_JVM', "")
                decrypt_secret = parse_apollo_secret_jvm(apollo_encrypt_jvm).get("password", "9i2x7DBpdWSe3XaJ")
            spilt_val = re.match("ENC\((.*?)\)", apollo_value.strip())
            if decrypt_secret and spilt_val:
                val = decrypt_pbe_with_hmac_sha512_aes_256(spilt_val.group(1), decrypt_secret)
            else:
                val = apollo_value
            return val

        return wrapper

    return inner
