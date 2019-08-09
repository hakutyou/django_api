import base64

import requests

from api.shortcuts import Response
from external.interface import baidu_face_service, baidu_vision_service, baidu_ocr_service


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


def face_detect(url):
    image_base64 = base64.b64encode(requests.get(url).content)
    data = {
        'image': image_base64,
        'image_type': 'BASE64',
        'face_field': 'quality',
        'face_type': 'LIVE',
        'liveness_control': 'NORMAL',
    }
    response = baidu_face_service.post('/rest/2.0/face/v3/detect', data=data)
    if response['result']:
        face_list = response['result']['face_list']
        for face_item in face_list:
            quality = face_item['quality']
            detect_occlusion = {
                'left_eye': 0.6,
                'right_eye': 0.6,
                'nose': 0.7,
                'mouth': 0.7,
                'left_cheek': 0.8,
                'right_cheek': 0.8,
                'chin_contour': 0.6,
            }
            detect_angle = {
                'yaw': 20,
                'pitch': 20,
                'roll': 20,
            }
            error_response = []
            for i in detect_angle:
                if face_item['angle'][i] > detect_angle[i]:
                    error_response.append(i)
            for i in detect_occlusion:
                if quality['occlusion'][i] > detect_occlusion[i]:
                    error_response.append(i)
            if quality['blur'] >= 0.7:
                error_response.append('blur')
            if quality['illumination'] <= 40:
                error_response.append('illumination')
            if quality['completeness'] == 0:
                error_response.append('completeness')
            if error_response:
                return Response(280, data=error_response)
    return response
