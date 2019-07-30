import base64

import requests

from external.interface import baidu_service


def image_detect(url):
    image_base64 = base64.b64encode(requests.get(url).content)
    data = {
        'image': image_base64,
    }
    response = baidu_service.post('/rest/2.0/image-classify/v2/advanced_general', data=data)
    return response
