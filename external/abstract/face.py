import base64

import requests
from django.conf import settings

from api.exception import ClientError
from external.interface import tencent_face, baidu_face
from image.models import FaceUser
from utils import random_string


class FaceService:
    def __init__(self):
        self.tencent_face_service = tencent_face.TencentFaceService(appid=settings.TENCENT_AI_APPID,
                                                                    app_key=settings.TENCENT_AI_APPKEY)
        self.baidu_face_service = baidu_face.BaiduFaceService(client_id=settings.FACE_CLIENT_ID,
                                                              client_secret=settings.FACE_SECRET)

    def user_add(self, url, user_name, group_id='default', user_id=None):
        # TODO: 检测人脸合格
        # 检测人脸重复
        search = self.user_search(url)
        for i in search:
            if search[i] and search[i].get('score', 0) > 80:
                raise ClientError('人脸已经存在', 1)
        # 录入人脸
        user_id = user_id or random_string()
        image_base64 = base64.b64encode(requests.get(url).content)
        try:
            self.tencent_face_service.user_add(image_base64, user_name, group_id, user_id)
            self.baidu_face_service.user_add(image_base64, user_name, group_id, user_id)
        except ClientError as c:
            # TODO: baidu_delperson
            self.tencent_face_service.user_remove(user_id)
            raise ClientError(c.response, c.code)

        FaceUser.objects.create(user_name=user_name, user_id=user_id,
                                face_image=url, group_id=group_id)
        return {
            'user_id': user_id,
            'group_id': group_id,
            'user_name': user_name,
        }

    def user_remove(self, user_id, group_id='default'):
        tencent_response = self.tencent_face_service.user_remove(user_id)
        baidu_response = self.baidu_face_service.user_remove(user_id, group_id)
        FaceUser.objects.get(user_id=user_id).delete()
        return {
            'tencent_response': tencent_response,
            'baidu_response': baidu_response,
        }

    def user_search(self, url):
        image_base64 = base64.b64encode(requests.get(url).content)
        tencent_response = self.tencent_face_service.user_search(image_base64)
        baidu_response = self.baidu_face_service.user_search(image_base64)
        return {
            'tencent': tencent_response,
            'baidu': baidu_response,
        }
