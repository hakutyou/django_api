import hashlib

from api.shortcuts import Response


class WechatOfficial:
    def __init__(self, token):
        self.token = token

    def verify_token(self, request):
        data = {
            'token': self.token,
            'timestamp': request.GET.get('timestamp'),
            'nonce': request.GET.get('nonce'),
        }
        signature = []
        for i in data.values():
            signature.append(i)
        signature.sort()
        signature = hashlib.sha1(''.join(signature).encode()).hexdigest()
        print(signature)
        if signature == request.GET.get('signature'):
            return request.GET.get('echostr')
        else:
            return Response(1)
