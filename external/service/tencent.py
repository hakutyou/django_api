import hashlib
from typing import Union
from urllib import parse

import time

from utils.xrandom import random_string
from .base import BaseService


class TencentService(BaseService):
    base_url = 'https://api.ai.qq.com/'

    def __init__(self, appid, app_key):
        self.appid = appid
        self.app_key = app_key

    def post(self, interface: str, data: Union[dict, list] = None):
        data['app_id'] = self.appid
        data['time_stamp'] = int(time.time())
        data['nonce_str'] = random_string(length=32)
        self.sign(data)
        return super(TencentService, self).post(interface, data).json()

    def sign(self, data: dict) -> None:
        sorted_values = sorted(data.items(), key=lambda val: val[0])
        sorted_values = list(filter(lambda x: x[1] is not None, sorted_values))
        _montage = parse.urlencode(sorted_values)
        _montage += f'&app_key={self.app_key}'
        data['sign'] = hashlib.md5(_montage.encode('utf-8')).hexdigest().upper()
        return
