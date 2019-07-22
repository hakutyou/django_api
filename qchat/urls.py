# -*- coding: utf-8 -*-
from django.conf.urls import url

from .qchat import qchat

urlpatterns = [
    url(r'', qchat),
]
