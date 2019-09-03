import json

import requests
import time

from api.service import logger
from utils import string_color, protect_dict


class BaseService:
    base_url = ''

    def post(self, interface, data=None):
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
        if isinstance(data, dict):
            data = json.dumps(protect_dict(data), indent=4, ensure_ascii=False)
        if isinstance(result, dict):
            result = json.dumps(protect_dict(result), indent=4, ensure_ascii=False)
        logger.info(url,
                    extra={
                        'koto': 'request',
                        'duration': str(time_cost),
                        'method': 'POST',
                        'request': string_color(data, 'pink'),
                        'response': string_color(result, 'green')
                    })
        return response
