# -*- coding: utf-8 -*-
from django.conf.urls import url

from .recognition import general, ocr, face

urlpatterns = [
    # /image
    url(r'^recognition$', general.general_recognition),

    url(r'^face_verify$', face.face_verify),
    url(r'^face_compare$', face.face_compare),
    url(r'^face_detect$', face.face_detect),
    url(r'^user_add$', face.user_add),
    url(r'^user_remove$', face.user_remove),
    url(r'^user_search$', face.user_search),
    url(r'^user_list$', face.user_list),

    url(r'^ocr$', ocr.general_ocr),
]
