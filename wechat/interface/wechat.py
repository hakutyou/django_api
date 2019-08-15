import base64
import hashlib
import socket
import struct

import requests
import time
from Crypto.Cipher import AES
from bs4 import BeautifulSoup
from django.core.cache import cache

from api.shortcuts import Response
from utils import random_string


class WechatError(Exception):
    def __init__(self, errcode, errmsg):
        super(WechatError, self).__init__()
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return f'errcode: {self.errcode}, errmsg: {self.errmsg}'


class WechatOfficial:
    prefix_url = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, appid, appsecret, token, aes_key):
        self.aes_key = base64.b64decode(aes_key + '=')
        self.mode = AES.MODE_CBC
        self.appid = appid
        self.appsecret = appsecret
        self.token = token

    def verify_token(self, request):
        nonce = request.GET['nonce']
        data = {
            'token': self.token,
            'timestamp': request.GET['timestamp'],
            'nonce': nonce,
        }
        signature = []
        for i in data.values():
            signature.append(i)
        signature.sort()
        signature = hashlib.sha1(''.join(signature).encode()).hexdigest()
        if signature == request.GET.get('signature'):
            echostr = request.GET.get('echostr')
            if echostr:  # 接入微信
                return echostr
            # 实际信息
            openid = request.GET.get('openid')  # receive['FromUserName']
            msg_signature = request.GET.get('msg_signature')
            receive = self.xml_analyse(request.body.decode())
            if request.GET.get('encrypt_type') == 'aes':
                receive = self.xml_analyse(self.decrypt(receive['Encrypt']))
            # print(receive)
            ##########
            # 回复信息
            ##########
            # 整个过程需要 5 秒内完成，否则丢到 celery 异步运行并且直接返回 success
            # return 'success'
            create_time = int(time.time())
            data = {
                'ToUserName': receive['FromUserName'],
                'FromUserName': receive['ToUserName'],
                'CreateTime': create_time,
                'MsgType': 'text',
                'Content': 'Hello!',
            }
            response = {
                'Encrypt': self.encrypt(self.xml_generate(data)),
                'MsgSignature': msg_signature,
                'TimeStamp': create_time,
                'Nonce': nonce,
            }
            return self.xml_generate(response)
        else:
            return Response(1)

    @staticmethod
    def xml_analyse(xml):
        soup = BeautifulSoup(xml, features='xml')
        xml = soup.find('xml')
        if not xml:
            return {}
        # 将 XML 数据转化为 Dict
        data = dict([(item.name, item.text) for item in xml.find_all()])
        return data

    @staticmethod
    def xml_generate(data):
        xml = '<xml>'
        for i in data:
            xml += f'<{i}><![CDATA[{data[i]}]]></{i}>\n'
        xml += '</xml>'
        return xml

    @property
    def access_token(self):
        token = cache.get(f'wechat:access_token:{self.appid}')
        if token:
            return token
        url = f'{self.prefix_url}token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}'
        response = requests.get(url).json()
        access_token = response.get('access_token')
        if not access_token:
            raise WechatError(response.get('errcode'), response.get('errmsg'))
        # 有效期为 2 小时
        cache.set(f'wechat:access_token:{self.appid}', access_token, 6800)
        return access_token

    def decrypt(self, encrypt):
        cryptor = AES.new(self.aes_key, self.mode, self.aes_key[:16])
        plain_text = cryptor.decrypt(base64.b64decode(encrypt))
        pad = plain_text[-1]
        content = plain_text[16:-pad]
        xml_len = socket.ntohl(struct.unpack('I', content[:4])[0])
        xml_content = content[4: xml_len + 4]
        # from_appid = content[xml_len + 4:]
        return xml_content.decode('utf-8')

    def encrypt(self, text):
        block_size = 32
        cryptor = AES.new(self.aes_key, self.mode, self.aes_key[:16])
        data = random_string(length=16) + struct.pack('I', socket.htonl(len(text))).decode() + text + self.appid
        data_length = len(data)
        amount_to_pad = block_size - (data_length % block_size)
        if amount_to_pad == 0:
            amount_to_pad = block_size
        # 获得补位所用的字符
        pad = chr(amount_to_pad)
        data += pad * amount_to_pad
        # AES 加密
        ciphertext = cryptor.encrypt(data.encode())
        return base64.b64encode(ciphertext).decode()
