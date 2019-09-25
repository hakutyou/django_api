import json
from typing import Union

import requests
import time

from api.service import logger


class BaseService:
    base_url = ''

    def post(self, interface: str, data: Union[dict, list] = None):
        url = f'{self.base_url}{interface}'

        if isinstance(data, list):
            data = json.dumps(data, indent=4, ensure_ascii=False)

        time_begin = time.time()
        response = requests.post(url, data=data)
        time_cost = time.time() - time_begin
        try:
            result = json.loads(response.text)
        except AttributeError:
            result = response
        logger.info('request', extra={
            'uri': url,
            'koto': 'request',
            'duration': str(time_cost),
            'method': 'POST',
            'request': str(data),
            'response': str(result)
        })
        return response
