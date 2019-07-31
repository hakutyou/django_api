import requests
from django.core.cache import cache


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
        response = requests.post(url, data=data)
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
