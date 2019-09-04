import base64

import requests

from api.exception import ClientError
from external.interface.tencent import TencentService
from utils import random_string


class TencentFaceService(TencentService):
    def face_detect(self, url, mode=1):
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64.decode(),
            'mode': mode,
        }
        response = self.post('fcgi-bin/face/face_detectface', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        return response['data']

    def user_add(self, image_base64, person_name, group_id='default', person_id=None):
        person_id = person_id or random_string()
        data = {
            'group_ids': group_id,
            'person_id': person_id,
            'image': image_base64.decode(),
            'person_name': person_name,
        }
        response = self.post('fcgi-bin/face/face_newperson', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        return response['data']

    def user_remove(self, user_id):
        data = {
            'person_id': user_id,
        }
        response = self.post('fcgi-bin/face/face_delperson', data=data)
        return response

    def user_search(self, image_base64, group_id='default'):
        data = {
            'image': image_base64,
            'group_id': group_id,
            'topn': 1,
        }
        response = self.post('fcgi-bin/face/face_faceidentify', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        candidates = response['data']['candidates']
        if candidates:
            return {
                'user_id': candidates[0]['person_id'],
                'score': candidates[0]['confidence'],
            }
        return {}

    def face_listperson(self, group_id='default'):
        data = {
            'group_id': group_id,
        }
        response = self.post('fcgi-bin/face/face_getpersonids', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        return response['data']
