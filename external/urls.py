# -*- coding: utf-8 -*-
from django.urls import path

from external.interface import mail

urlpatterns = [
    # /external
    path('mail/send/', mail.send_mail),
]
