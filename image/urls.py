# -*- coding: utf-8 -*-
from django.conf.urls import url

from .recognition import general, ocr, face

urlpatterns = [
    url(r'^recognition$', general.general_recognition),
    url(r'^face_detect$', face.face_detect),
    url(r'^tencent/face_detect', face.tencent_face_detect),
    url(r'^face_verify$', face.face_verify),
    url(r'^face_compare$', face.face_compare),

    url(r'^tencent/face_add$', face.face_add),
    url(r'^tencent/face_del$', face.face_del),
    url(r'^tencent/face_identify$', face.face_identify),
    url(r'^tencent/face_list$', face.face_list),

    url(r'^ocr$', ocr.general_ocr),
    url(r'^tencent/ocr$', ocr.tencent_general_ocr),
]
