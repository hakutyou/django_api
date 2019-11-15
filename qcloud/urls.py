from django.urls import path, re_path

import qcloud.controller as qcloud_api

urlpatterns = [
    # api/qcloud/
    re_path(r'^list(?P<path>.*/)$', qcloud_api.qfile.get_file_list),
    re_path(r'^list(?P<path>.*)$', qcloud_api.qfile.get_file_info),
    path('upload/', qcloud_api.qfile.upload_file),
]
