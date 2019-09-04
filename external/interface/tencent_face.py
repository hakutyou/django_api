import base64

import requests

from api.exception import ClientError
from external.interface.tencent import TencentService
from image.models import FaceUser
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

    def face_newperson(self, url, person_name, group_id='default', person_id=None):
        person_id = person_id or random_string()
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'group_ids': group_id,
            'person_id': person_id,
            'image': image_base64.decode(),
            'person_name': person_name,
        }
        response = self.post('fcgi-bin/face/face_newperson', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        FaceUser.objects.create(user_name=person_name, user_id=person_id,
                                face_image=url, group_id=group_id)
        return response['data']

    def face_delperson(self, person_id):
        data = {
            'person_id': person_id,
        }
        response = self.post('fcgi-bin/face/face_delperson', data=data)
        FaceUser.objects.get(user_id=person_id).delete()
        return response

    def face_idperson(self, url, group_id='default'):
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64,
            'group_id': group_id,
            'topn': 5,
        }
        response = self.post('fcgi-bin/face/face_faceidentify', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        return response['data']

    def face_listperson(self, group_id='default'):
        data = {
            'group_id': group_id,
        }
        response = self.post('fcgi-bin/face/face_getpersonids', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        return response['data']
