# 加解密相关
# linux 使用 pycryptodome, Windows 使用 pycryptodomex 库
import base64
from typing import Union

from Crypto.Hash import keccak, SHA1, MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def message_digest(message: str, method: str = 'keccak', bits: int = 224) -> str:
    """
    信息摘要算法, 可以使用的包括
    md5-16|32, Keccak-224|256|384|512
    """
    k = keccak.new(digest_bits=224)
    return k.update(message.encode('utf-8')).hexdigest()


def rsa_signature(message: str, pem: str, crypt_via='sha1') -> Union[str, None]:
    """
    RSA 签名
    crypt_via 可以是 sha1, md5
    """
    crypt_mapping = {
        'sha1': SHA1,  # RSA with SHA1
        'md5': MD5,  # RSA with MD5
    }
    private_key = RSA.importKey(pem)
    cipher = PKCS1_v1_5.new(private_key)  # PKCS1_v1_5 填充
    h = crypt_mapping.get(crypt_via, SHA1).new(message.encode('utf-8'))
    if cipher.can_sign():
        signature = cipher.sign(h)
    else:
        return None
    return base64.b64encode(signature).decode('utf-8')


# 测试
if __name__ == '__main__':
    import json

    print(message_digest('123'))
    pem = '''-----BEGIN PRIVATE KEY-----
        MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKd3zf0cyJkirVJ6
        ecWhATeWGlhjxYbvSbyYdQ7LZpat+Ac2fSPxWG6x9ndt5AC9IWYLo6EgOIVwav9z
        RKNQ8RCaTKadZXCS8vTXTkneZjNwcFyraIk950oLO2poMmxVBwohvTq2XE2IFlNb
        nRVJnUjZkDzK8yPZZbymC/Ou8KfRAgMBAAECgYBb+o41lciLayNc6I3XQN3lRNkF
        cQ79VJHgNrAcRxT6b2SJuaCzzAuxCKeA4udWjIo6fOwLRCInEB6EXS/2ry8m9oO4
        JY8gqa5QEyS58JCxXRbA9xlzK9qW8bs4p9afGmnfnbWmKe/IPBcm1XZmXHzkzcuK
        mjNMoMn3EHBHsyf3wQJBANpgBj8WCZZgJWYSmPKsqBIcJZIHuoQfC/kZOEyGKngt
        WGfJToIj53NPpjTq9nSY3R7pusZuTvxStH13E/f7QrkCQQDEUmVX1hF8f7zG5Igf
        rJYwAczClEL6WPfO4WFjj1x51f0W0hsEzeh32htvIX9F4JoqjLsWQ6Z8JX0irRF5
        lWHZAkAP5OFPgikces7+COh88TgiaU4KvOlEaIYUkVNZroI00QgYNbyzGC3mZKuy
        Ok/J2L5vW4+ulaTGFLbyUtJvQChxAkBC28i1rCqSWrJAje2p083mFYbVMUbKGWhz
        ZSAUlusodu7VScJ31WP5BSdYpnDArGf0W68POwTEvMOr/oK4BF6pAkAM+SNXhw9d
        POP/06u5sZrAIlVydhvvo77pXEo1cZQipWeEyj86e+AP/q7ECuQ7X5CZN9FsCWbX
        8LhyvAXTfr7F
        -----END PRIVATE KEY-----
        '''
    content = json.dumps({'text': 'あぁ'}, sort_keys=True)
    print(rsa_signature(content, pem, crypt_via='sha1'))
    # 'LH8W/rwVr8buqnVaXmtz9I1J+whc03s5cv25zd1SXDMd3FRNLqLxaLkDiZQ8ssW8J4gH'
    # 'eHcKDe7aWJhb/Nfx4gOTfzuRtiDaDSUxDNppHmkXSA5wjQvMbKMCkRWH/Tw5OOe6fNcB'
    # 'QM7PIZH9H8rOBdZcaP6tUrIafr6QKmsWHw0='
