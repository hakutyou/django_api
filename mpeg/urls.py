# -*- coding: utf-8 -*-
from django.urls import path

from .controller import bilibili

urlpatterns = [
    # disabled
    # api/mpeg/
    # path('ffprobe/format', probe.show_format),
    # path('ffprobe/streams', probe.show_streams),
    path('bilibili/info', bilibili.get_video_info),
    path('bilibili/get', bilibili.get_video),
    path('bilibili/check', bilibili.get_video_check),
]
