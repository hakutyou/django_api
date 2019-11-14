import json
from asyncio import Future
from typing import Union

import requests
from requests_futures.sessions import FuturesSession

from api.service import logger
from utils import xtime
from utils.utils import protect_dict


class BaseService:
    base_url = ''

    def async_post(self, interface: str, data: Union[dict, list] = None) -> Future:
        """
        异步 POST，最好不要关心返回结果
        也可以通过 .result() 强行获取结果（不写日志）
        """
        url = f'{self.base_url}{interface}'

        if isinstance(data, list) or isinstance(data, dict):
            pretty_data = json.dumps(protect_dict(data), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            pretty_data = str(data)

        logger.info('request_send_async', extra={
            'uri': url,
            'method': 'POST',
            'request': pretty_data,
        })
        return FuturesSession().post(url=url, data=data)

    def post(self, interface: str, data: Union[dict, list] = None):
        url = f'{self.base_url}{interface}'

        if isinstance(data, list) or isinstance(data, dict):
            pretty_data = json.dumps(protect_dict(data), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            pretty_data = str(data)

        logger.info('request_send', extra={
            'uri': url,
            'method': 'POST',
            'request': pretty_data,
        })
        time_begin = xtime.now()
        response = requests.post(url, data=data)
        time_cost = xtime.now() - time_begin
        try:
            result = json.loads(response.text)
        except AttributeError:
            result = response

        if isinstance(result, dict):
            pretty_result = json.dumps(protect_dict(result), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            pretty_result = str(result)
        logger.info('request_receive', extra={
            'uri': url,
            'duration': str(time_cost.total_seconds()),
            'response': pretty_result,
        })
        return response
