# -*- coding: utf-8 -*-
from django.urls import path

from record.controller import score
from . import views

urlpatterns = [
    # api/data/
    path('dict/kana/', views.dict_kana_item_view),
    path('dict/kanji/', views.dict_kanji_item_view),
    # new dict push to dict_score_table
    path('score/get/', score.score_get),
    path('score/set/', score.score_set),
    path('score/review/', score.score_review),
]
