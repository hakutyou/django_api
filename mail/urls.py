# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import send_mail

urlpatterns = [
    url(r'', send_mail),
]
