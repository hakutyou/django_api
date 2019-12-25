# -*- coding: utf-8 -*-
from django.urls import path, re_path

from external.interface import mail, scf

urlpatterns = [
    # api/external/
    path('mail/send/', mail.send_mail),
    re_path('scf/(?P<path>.*)$', scf.scf_common),
    path('proxy/', scf.proxy_common),
]
