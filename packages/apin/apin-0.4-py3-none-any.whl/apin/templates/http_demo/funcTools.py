"""
============================
Author:柠檬班-木森
Time:2021/6/5 20:35
E-mail:3247119728@qq.com
Company:湖南零檬信息技术有限公司
=======
"""
import base64

import rsa
from apin.core.tools import *
from tests.hooks.fixture_hook import *
from tests.hooks.db_check_hook import *
import random


def rand_phone(phone='177'):
    for i in range(8):
        phone += str(random.randint(0, 9))
    return str(phone)


def get_timestamp():
    """获取时间戳"""
    return time.time()


def ras_encrypt(msg, server_pub):
    """
    rsa加密
    :param msg: 待加密文本
    :param server_pub: 密钥
    :return:
    """
    msg = msg.encode('utf-8')
    pub_key = server_pub.encode("utf-8")
    public_key_obj = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key)  #
    cryto_msg = rsa.encrypt(msg, public_key_obj)  # 生成加密文本
    cipher_base64 = base64.b64encode(cryto_msg)  # 将加密文本转化为 base64 编码
    return cipher_base64.decode()


def get_sign(timestamp, token):
    """获取签名"""
    server_pub = """
        -----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
        O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
        tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
        kKlZFc8Br7SHtbL2tQIDAQAB
        -----END PUBLIC KEY-----
        """
    # 获取token前50位
    prefix_50_token = token[:50]
    msg = prefix_50_token + str(timestamp)
    return ras_encrypt(msg, server_pub)
