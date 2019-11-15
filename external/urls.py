# -*- coding: utf-8 -*-
from django.urls import path

from external.interface import mail

urlpatterns = [
    # api/external/
    path('mail/send/', mail.send_mail),
]
