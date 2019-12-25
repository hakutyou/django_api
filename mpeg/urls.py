# -*- coding: utf-8 -*-
from django.urls import path

from .controller import probe

urlpatterns = [
    # disabled
    # api/ffmpeg/
    path('ffprobe/format', probe.show_format),
    path('ffprobe/streams', probe.show_streams),
]
