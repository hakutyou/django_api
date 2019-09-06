from typing import Union

from django.core.cache import cache

from external.interface.base import BaseService


class BaiduService(BaseService):
    base_url = 'https://aip.baidubce.com/'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def post(self, interface: str, data: Union[dict, list] = None, get_data: dict = None, get_access: bool = True):
        interface = f'{interface}?'
        if get_access:
            interface += f'access_token={self.access_token}&'
        if get_data is not None:
            for i in get_data:
                interface += f'{i}={get_data[i]}&'
        return super(BaiduService, self).post(interface, data).json()

    @property
    def access_token(self) -> str:
        access_token = cache.get(f'baidu:access_token:{self.client_id}')
        if not access_token:
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
            response = self.post('oauth/2.0/token', get_data=data, get_access=False)
            access_token = response['access_token']
            cache.set(f'baidu:access_token:{self.client_id}', access_token, response['expires_in'] - 3600)
        return access_token
