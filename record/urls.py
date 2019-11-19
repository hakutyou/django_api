# -*- coding: utf-8 -*-
from django.urls import path

from . import views

urlpatterns = [
    # api/data/
    path('dict/kana/', views.dict_kana_item_view),
    path('dict/kanji/', views.dict_kanji_item_view),
]
