import base64

import requests

from .baidu import BaiduService


class BaiduVisionService(BaiduService):
    def image_detect(self, url):
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64,
        }
        response = self.post('rest/2.0/image-classify/v2/advanced_general', data=data)['result']
        max_ret = max(response, key=lambda x: x['score'])
        return max_ret
