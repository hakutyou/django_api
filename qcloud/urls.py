from django.conf.urls import url

import qcloud.controller as qcloud_api

urlpatterns = [
    url(r'^list(?P<path>.*/)$', qcloud_api.qfile.get_file_list),
    url(r'^list(?P<path>.*)$', qcloud_api.qfile.get_file_info),
]
