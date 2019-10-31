# -*- coding: utf-8 -*-
from django.urls import path

from .recognition import general, ocr, face

urlpatterns = [
    # /image
    path('recognition/', general.general_recognition),

    path('face_verify/', face.face_verify),
    path('face_compare/', face.face_compare),
    path('face_detect/', face.face_detect),
    path('user_add/', face.user_add),
    path('user_remove/', face.user_remove),
    path('user_search/', face.user_search),
    path('user_list/', face.user_list),

    path('ocr/', ocr.general_ocr),
]
