# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # data/
    url(r'^record/$', views.record_item_view),
]
