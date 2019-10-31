# -*- coding: utf-8 -*-
from django.urls import path

from external.interface import mail

urlpatterns = [
    # /external
    path('send_mail', mail.send_mail),
]
