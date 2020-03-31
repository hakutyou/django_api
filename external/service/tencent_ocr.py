import base64

import requests

from .tencent import TencentService


class TencentOCRService(TencentService):
    def ocr_general(self, url, lang):
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64.decode(),
        }
        response = self.post('fcgi-bin/ocr/ocr_generalocr', data=data)['data']['item_list']
        ret = []
        for i in response:
            ret.append(i['itemstring'])
        return ret
