# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    # api/data/
    path('record/', views.record_item_view),
]
