import json

import requests
import time
from django.core.cache import cache

from api.service import logger
from utils import string_color, protect_dict


class BaiduService:
    base_url = 'https://aip.baidubce.com'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def post(self, interface, data=None, get_data=None, get_access=True):
        url = f'{self.base_url}{interface}?'
        if get_access:
            url += f'access_token={self.access_token}&'
        if get_data is not None:
            for i in get_data:
                url += f'{i}={get_data[i]}&'

        time_begin = time.time()
        response = requests.post(url, data=data)
        time_cost = time.time() - time_begin

        try:
            result = json.loads(response.text)
        except AttributeError:
            result = response

        if type(data == dict):
            data = json.dumps(protect_dict(data), indent=4, ensure_ascii=False)
        if type(result == dict):
            result = json.dumps(protect_dict(result), indent=4, ensure_ascii=False)

        logger.info(url,
                    extra={
                        'koto': 'request',
                        'duration': str(time_cost),
                        # 'receive_time': datetime.fromtimestamp(time_begin).strftime('%Y-%m-%d %H:%M:%S')
                        'method': 'POST',
                        'data': string_color(data, 'pink'),
                        # 'cookies': request.COOKIES,
                        'response': string_color(result, 'green')
                    })
        return response.json()

    @property
    def access_token(self):
        access_token = cache.get(f'baidu:access_token:{self.client_id}')
        if not access_token:
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
            response = self.post('/oauth/2.0/token', get_data=data, get_access=False)
            access_token = response['access_token']
            cache.set('baidu:access_token', access_token, response['expires_in'] - 3600)
        return access_token
