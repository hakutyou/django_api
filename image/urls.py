# -*- coding: utf-8 -*-
from django.conf.urls import url

from .recognition import general, ocr

urlpatterns = [
    url(r'recognition', general.general_recognition),
    url(r'ocr', ocr.general_ocr),
]
