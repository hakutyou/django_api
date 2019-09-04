import hashlib
from urllib import parse

import time

from external.interface.base import BaseService
from utils import random_string


class TencentService(BaseService):
    base_url = 'https://api.ai.qq.com/'

    def __init__(self, appid, app_key):
        self.appid = appid
        self.app_key = app_key

    def post(self, interface, data=None):
        data['app_id'] = self.appid
        data['time_stamp'] = int(time.time())
        data['nonce_str'] = random_string(length=32)
        self.sign(data)
        return super(TencentService, self).post(interface, data).json()

    def sign(self, data):
        sorted_values = sorted(data.items(), key=lambda val: val[0])
        _montage = parse.urlencode(sorted_values)
        _montage += f'&app_key={self.app_key}'
        data['sign'] = hashlib.md5(_montage.encode('utf-8')).hexdigest().upper()
        return
