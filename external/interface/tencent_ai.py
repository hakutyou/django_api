import base64

import requests

from external.interface.tencent import TencentService


class TencentAIService(TencentService):
    def face_detect(self, url, mode=1):
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64.decode(),
            'mode': mode,
        }
        response = self.post('fcgi-bin/face/face_detectface', data=data)
        return response

    def ocr_general(self, url):
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64.decode(),
        }
        response = self.post('fcgi-bin/ocr/ocr_generalocr', data=data)
        return response
