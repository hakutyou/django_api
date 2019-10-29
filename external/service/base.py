import json
from typing import Union

import requests
import time

from api.service import logger
from utils.utils import protect_dict


class BaseService:
    base_url = ''

    def post(self, interface: str, data: Union[dict, list] = None):
        url = f'{self.base_url}{interface}'

        if isinstance(data, list) or isinstance(data, dict):
            pretty_data = json.dumps(protect_dict(data), indent=2, sort_keys=True, ensure_ascii=False)
        else:
            pretty_data = str(data)

        logger.info('request_send', extra={
            'uri': url,
            'koto': 'request_send',
            'method': 'POST',
            'request': pretty_data,
        })
        time_begin = time.time()
        response = requests.post(url, data=data)
        time_cost = time.time() - time_begin
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
            'koto': 'request_receive',
            'duration': str(time_cost),
            'response': pretty_result,
        })
        return response
