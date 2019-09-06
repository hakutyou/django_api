# -*- coding: utf-8 -*-
from django.conf.urls import url

from external.interface import mail

urlpatterns = [
    url(r'send_mail', mail.send_mail),
]
