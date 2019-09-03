import base64

import requests

from external.interface.baidu import BaiduService


class BaiduFaceService(BaiduService):
    detect_occlusion = {
        'left_eye': lambda x: x > 0.6,
        'right_eye': lambda x: x > 0.6,
        'nose': lambda x: x > 0.7,
        'mouth': lambda x: x > 0.7,
        'left_cheek': lambda x: x > 0.8,
        'right_cheek': lambda x: x > 0.8,
        'chin_contour': lambda x: x > 0.6,
    }

    detect_angle = {
        'yaw': lambda x: x > 20,
        'pitch': lambda x: x > 20,
        'roll': lambda x: 10 <= abs(x % 90) <= 80,
    }
    detect_location = {
        'width': lambda x: x < 200,
        'height': lambda x: x < 200,
    }
    detect_quality = {
        'blur': lambda x: x >= 0.7,
        'illumination': lambda x: x <= 40,
        'completeness': lambda x: x == 0,
    }

    def face_verify(self, url, field=''):
        """
        在线活体检测
        """
        image_base64 = base64.b64encode(requests.get(url).content)
        data = {
            'image': image_base64,
            'image_type': 'BASE64',
            'face_field': field,
            'option': 'COMMON',
        }
        response = self.post('/rest/2.0/face/v3/detect', data=data)
        return response

    def face_compare(self, url_1, url_2):
        """
        人脸对比
        """
        # image_base64_1 = base64.b64encode(requests.get(url_1).content)
        # image_base64_2 = base64.b64encode(requests.get(url_2).content)
        data = [
            {
                # 'image': image_base64_1,
                # 'image_type': 'BASE64',
                'image': url_1,
                'image_type': 'URL',
                'face_type': 'LIVE',
                'quality_control': 'NORMAL',  # 图片质量控制
                'liveness_control': 'NORMAL',  # 活体检测控制
            },
            {
                # 'image': image_base64_2,
                # 'image_type': 'BASE64',
                'image': url_2,
                'image_type': 'URL',
                'face_type': 'LIVE',
                'quality_control': 'NORMAL',  # 图片质量控制
                'liveness_control': 'NORMAL',  # 活体检测控制
            }
        ]
        response = self.post('/rest/2.0/face/v3/match', data=data)
        return response

    def face_detect(self, url, field=''):
        """
        人脸检测
        """
        image_base64 = base64.b64encode(requests.get(url).content)
        face_field = 'quality,' + field
        data = {
            'image': image_base64,
            'image_type': 'BASE64',
            'face_field': face_field,
            'face_type': 'LIVE',
            'liveness_control': 'NORMAL',
        }
        response = self.post('/rest/2.0/face/v3/detect', data=data)
        if response['result']:
            face_list = response['result']['face_list']
            count = 0
            for face_item in face_list:
                quality = face_item['quality']

                error_response = []
                for i in self.detect_angle:
                    if self.detect_angle[i](face_item['angle'][i]):
                        error_response.append(i)
                for i in self.detect_occlusion:
                    if self.detect_occlusion[i](quality['occlusion'][i]):
                        error_response.append(i)
                for i in self.detect_location:
                    if self.detect_location[i](face_item['location'][i]):
                        error_response.append(i)
                for i in self.detect_quality:
                    if self.detect_quality[i](quality[i]):
                        error_response.append(i)

                if error_response:
                    face_list[count] = {
                        'error': error_response,
                    }
                count += 1
        return response
