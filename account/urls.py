from django.conf.urls import url
from rest_framework_simplejwt import views as jwt_views

from . import views
from .controller import sms, user

urlpatterns = [
    url(r'^sms_send/register$', sms.sms_sender('register')),
    url(r'^sms_send/reset_password', sms.sms_sender('reset_password')),
    url(r'^user/$', views.user_view),
    url(r'^login/$', views.login_view),
    url(r'^password/reset/$', user.reset_password),
    url(r'^password/modify/$', user.modify_password),
    url(r'^refresh/$', jwt_views.token_refresh),
]
