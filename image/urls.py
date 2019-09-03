# -*- coding: utf-8 -*-
from django.conf.urls import url

from .recognition import general, ocr, face

urlpatterns = [
    url(r'^recognition$', general.general_recognition),
    url(r'^face_detect$', face.face_detect),
    url(r'^face_verify$', face.face_verify),
    url(r'^face_compare$', face.face_compare),
    url(r'^ocr$', ocr.general_ocr),
]
