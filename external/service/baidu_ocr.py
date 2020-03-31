import base64

import requests

from .baidu import BaiduService


class BaiduOCRService(BaiduService):
    def ocr_general(self, url, lang):
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64,
            # CHN_ENG ENG POR FRE GER ITA SPA RUS JAP KOR
            'language_type': lang,
            'detect_direction': True,
            'detect_language': True,
            'probability': False,
        }
        response = self.post('rest/2.0/ocr/v1/general_basic', data=data)['words_result']
        ret = []
        for i in response:
            ret.append(i['words'])
        return ret
