from django.conf.urls import url

import qcloud.controller as qcloud_api

urlpatterns = [
    url(r'^get_file_list/(.*)$', qcloud_api.qfile.get_file_list),
    url(r'^get_file_info/(.*)$', qcloud_api.qfile.get_file_info),
]
