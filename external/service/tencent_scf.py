import base64
import hashlib
import hmac
from typing import Union

from external.service.base import BaseService
from utils import xtime, xrandom


class TencentSCFService(BaseService):
    base_url = 'https://scf.hakutyou.xyz/release/'

    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key

    def post(self, interface: str, data: Union[dict, list] = None, headers=None):
        if headers is None:
            headers = {}
        self.sign(headers)
        response = super(TencentSCFService, self).post(interface, data, headers=headers)
        # json 自动变成 dict
        if isinstance(response, dict):
            return response
        # 错误或文本返回 text
        return response.text

    def sign(self, headers: dict) -> None:
        headers['date'] = str(xtime.to_timestamp(xtime.now()))
        headers['nonce'] = xrandom.random_string()
        # 签名
        encrypt_header_str = ''
        joint_str = ''
        for i in headers:
            encrypt_header_str += i + ' '
            joint_str += f'{i}: {headers[i]}\n'
        h = hmac.new(self.secret_key.encode(encoding='utf-8'), joint_str[:-1].encode(encoding='utf-8'), hashlib.sha1)
        signature = base64.b64encode(h.digest()).decode()
        headers['Authorization'] = f'hmac id="{self.secret_id}", algorithm="hmac-sha1", ' \
                                   f'headers="{encrypt_header_str[:-1]}", signature="{signature}"'
