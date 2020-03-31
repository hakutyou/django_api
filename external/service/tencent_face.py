from api.exception import ClientError
from utils.xrandom import random_string
from .tencent import TencentService
from .virtual_face import VirtualFace


class TencentFaceService(TencentService, VirtualFace):
    # 不使用腾讯的人脸检测，很容易返回 image size too big

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
            return False
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
            return response['msg']
        candidates = response['data']['candidates']
        if candidates:
            return {
                'user_id': candidates[0]['person_id'],
                'score': candidates[0]['confidence'],
            }
        return None

    def user_list(self, group_id='default'):
        data = {
            'group_id': group_id,
        }
        response = self.post('fcgi-bin/face/face_getpersonids', data=data)
        if response['msg'] != 'ok':
            raise ClientError(response['msg'], code=1)
        return response['data']['person_ids']
