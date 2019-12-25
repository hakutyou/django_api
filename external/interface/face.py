import base64

import requests

from api.exception import ClientError
from external.service import tencent_face_service, baidu_face_service
from image.models import FaceUser
from utils.xrandom import random_string


class FaceService:
    def __init__(self):
        self.face_service_list = {
            'tencent': tencent_face_service,
            'baidu': baidu_face_service,
        }

    def face_detect(self, url):
        data = {}
        for i in self.face_service_list:
            data[i] = self.face_service_list[i].face_detect(url)
        return data

    def user_add(self, url, user_name, group_id='default', user_id=None):
        # 检测人脸合格
        detect_dict = self.face_detect(url)
        for i in detect_dict:
            if not detect_dict[i]:
                raise ClientError(f'{i} 人脸检测不通过')

        # 检测人脸重复
        search = self.user_search(url)
        for i in search:
            if isinstance(search[i], dict) and search[i].get('score', 0) > 80:
                raise ClientError('人脸已经存在', 1)
        # 录入人脸
        user_id = user_id or random_string()
        image_base64 = base64.b64encode(requests.get(url).content)

        user_add_list = []
        face_token = None
        for i in self.face_service_list:
            response = self.face_service_list[i].user_add(image_base64, user_name, group_id, user_id)
            if not response:
                for j in user_add_list:
                    self.face_service_list[j].user_remove(user_id)
                raise ClientError(f'{i} 录入失败', 1)
            # 百度需要记录 face_token
            if i == 'baidu':
                face_token = response['face_token']
            user_add_list.append(i)

        # 写入数据库
        FaceUser.objects.create(user_name=user_name, user_id=user_id,
                                face_image=url, group_id=group_id, face_token=face_token)
        return {
            'user_id': user_id,
            'group_id': group_id,
            'user_name': user_name,
        }

    def user_remove(self, user_id):
        ret = {}
        for i in self.face_service_list:
            ret[i] = self.face_service_list[i].user_remove(user_id)
        FaceUser.objects.get(user_id=user_id).delete()
        return ret

    def user_search(self, url, all_need=False):
        image_base64 = base64.b64encode(requests.get(url).content)
        ret = {}
        for i in self.face_service_list:
            ret[i] = self.face_service_list[i].user_search(image_base64)
            if ret[i].get('score', 0) > 80:
                if not all_need:
                    return ret[i]
        if all_need:
            ret_set = set(map(lambda x: x['user_id'], ret.values()))
            if len(ret_set) == 1:
                score = list(map(lambda x: x['score'], ret.values()))
                return {
                    'user_id': list(ret_set)[0],
                    'score': int(sum(score) / len(score))
                }
        return False

    def user_list(self) -> dict:
        ret = {}
        for i in self.face_service_list:
            ret[i] = self.face_service_list[i].user_list()
        return ret

    def face_verify(self, url) -> dict:
        ret = {}
        for i in self.face_service_list:
            ret[i] = self.face_service_list[i].face_verify(url)
        return ret

    def face_compare(self, url1, url2) -> dict:
        ret = {}
        for i in self.face_service_list:
            ret[i] = self.face_service_list[i].face_compare(url1, url2)
        return ret
