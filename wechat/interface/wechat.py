import hashlib

import requests
from django.core.cache import cache

from api.shortcuts import Response


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
        self.appid = appid
        self.appsecret = appsecret
        self.token = token
        self.aes_key = aes_key

    def verify_token(self, request):
        data = {
            'token': self.token,
            'timestamp': request.GET['timestamp'],
            'nonce': request.GET['nonce'],
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
            openid = request.GET.get('openid')
            encrypt_type = request.GET.get('encrypt_type')
            msg_signature = request.GET.get('msg_signature')
            print(request.body)
            return Response(0)
        else:
            return Response(1)

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
