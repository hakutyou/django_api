from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    url(r'^login/$', views.login_view),
    url(r'^refresh/$', jwt_views.token_refresh),
    url(r'^user/$', views.user_view),
]
