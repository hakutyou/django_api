# -*- coding: utf-8 -*-
from django.conf.urls import url

from .interface import wechat_official

urlpatterns = [
    url(r'^$', wechat_official.verify_token),
]
