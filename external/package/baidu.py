import base64

import requests

from external.interface import baidu_vision_service, baidu_ocr_service


def image_detect(url):
    image_base64 = base64.b64encode(requests.get(url).content)
    data = {
        'image': image_base64,
    }
    response = baidu_vision_service.post('/rest/2.0/image-classify/v2/advanced_general', data=data)
    return response


def ocr_basic(url, lang):
    image_base64 = base64.b64encode(requests.get(url).content)
    data = {
        'image': image_base64,
        # CHN_ENG ENG POR FRE GER ITA SPA RUS JAP KOR
        'language_type': lang,
        'detect_direction': True,
        'detect_language': True,
        'probability': False,
    }
    response = baidu_ocr_service.post('/rest/2.0/ocr/v1/general_basic', data=data)
    return response
