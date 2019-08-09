# -*- coding: utf-8 -*-
from django.conf.urls import url

from .recognition import general, ocr, face

urlpatterns = [
    url(r'^recognition$', general.general_recognition),
    url(r'^face_detect$', face.face_detect),
    url(r'^ocr$', ocr.general_ocr),
]
