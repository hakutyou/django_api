import json
from asyncio import Future
from contextlib import closing
from typing import Union

import requests
from requests_futures.sessions import FuturesSession

from api.exception import ClientError
from api.service import logger
from utils import xtime
from utils.utils import protect_dict_or_list


class BaseService:
    base_url = ''

    def async_post(self, interface: str, data: Union[dict, list] = None) -> Future:
        """
        异步 POST，最好不要关心返回结果
        也可以通过 .result() 强行获取结果（不写日志）
        """
        url = f'{self.base_url}{interface}'

        if isinstance(data, list) or isinstance(data, dict):
            pretty_data = json.dumps(protect_dict_or_list(data), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            pretty_data = str(data)

        logger.info('request_send_async', extra={
            'uri': url,
            'method': 'POST',
            'request': pretty_data,
        })
        return FuturesSession().post(url=url, data=data)

    def get(self, interface: str, data: Union[dict, list] = None, headers=None):
        return self.request(interface, data, headers, method='GET')

    def post(self, interface: str, data: Union[dict, list] = None, headers=None):
        return self.request(interface, data, headers, method='POST')

    def download(self, interface: str, fd, headers=None):
        url = f'{self.base_url}{interface}'

        with closing(requests.get(url, headers=headers, stream=True)) as res:
            for chunk in res.iter_content(chunk_size=1024):
                fd.write(chunk) if chunk else None

    def request(self, interface: str, data: Union[dict, list] = None, headers=None, method=None):
        url = f'{self.base_url}{interface}'

        if isinstance(data, list) or isinstance(data, dict):
            pretty_data = json.dumps(protect_dict_or_list(data), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            pretty_data = str(data)

        logger.info('request_send', extra={
            'uri': url,
            'method': 'POST',
            'request': pretty_data,
        })
        time_begin = xtime.now()
        if isinstance(data, list):
            if method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            else:
                response = requests.get(url, json=data, headers=headers)
        else:
            if method == 'POST':
                response = requests.post(url, data=data, headers=headers)
            else:
                response = requests.get(url, data=data, headers=headers)
        time_cost = xtime.now() - time_begin
        # 检查返回值
        if response.status_code >= 400:
            raise ClientError('服务器连接错误，请稍后再试')
        try:
            result = json.loads(response.text)
        except AttributeError:
            result = response

        if isinstance(result, dict):
            pretty_result = json.dumps(protect_dict_or_list(result), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            pretty_result = str(result)
        logger.info('request_receive', extra={
            'uri': url,
            'duration': str(time_cost.total_seconds()),
            'response': pretty_result,
        })
        return response
