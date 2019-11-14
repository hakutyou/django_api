# -*- coding: utf-8 -*-
from django.urls import path

from .recognition import general, ocr, face

urlpatterns = [
    # /image
    path('recognition/', general.general_recognition),

    path('face/verify/', face.face_verify),
    path('face/compare/', face.face_compare),
    path('face/detect/', face.face_detect),
    path('user/add/', face.user_add),
    path('user/remove/', face.user_remove),
    path('user/search/', face.user_search),
    path('user/list/', face.user_list),

    path('ocr/', ocr.general_ocr),
]
