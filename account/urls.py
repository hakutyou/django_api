from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views
from .controller import sms, user

urlpatterns = [
    # api/account/
    path('sms/register/', sms.sms_sender('register')),
    path('sms/reset_password/', sms.sms_sender('reset_password')),
    path('user/', views.user_view),
    path('login/', views.login_view),
    path('password/reset/', user.reset_password),
    path('password/modify/', user.modify_password),
    path('refresh/', jwt_views.token_refresh),

    path('captcha/', user.get_captcha),
    path('captcha/check', user.check_captcha),
]
