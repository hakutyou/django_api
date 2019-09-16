"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import datetime
import os

from decouple import config
from pythonjsonlogger import jsonlogger

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u*pc@ipsx3g=+1c3m)da9s&+$e_+9a$&o+-@x9ne^%^71qmk%%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# 0. 基本配置
ALLOWED_HOSTS = ['*']  # 允许访问的 IP
ROOT_URLCONF = 'api.urls'  # 根目录 URL
WSGI_APPLICATION = 'api.wsgi.application'

# 1. 应用配置（影响 Model）
INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'corsheaders',
    'account',
    'external',
    'qcloud',
    'image',
    'record',
    # 'mongolog',
]

AUTH_USER_MODEL = 'account.UserModels'

# 2. 中间件配置
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.EnhanceMiddleware',
]

# 3. 跨域访问配置
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_REGEX_WHITELIST = [
    'https?://emilia.fun',
]

# 4. 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# 5.日志配置
def filter_request(levelname, koto=None):
    def _filter_request(record):
        if record.levelname != levelname:
            return False
        if koto and record.koto != koto:
            """
            koto == request 表示向其他服务器发送 Request
            koto == reponse 表示接受 Request 返回 Response
            """
            return False
        return True

    return _filter_request


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'loggers': {  # 5.1 总览
        # 'django.db.backends': {
        #     'handlers': ['sql'],
        #     'propagate': False,
        #     'level': 'DEBUG'
        # },
        'api': {  # 项目内的 logger.info
            'handlers': ['error_console', 'warning_console', 'info_console_json'],
            'propagate': False,
            'level': 'DEBUG',
        }
    },
    'handlers': {  # 5.2 处理信息
        'sql': {
            # 输出到 stderr
            'class': 'logging.StreamHandler',
            'filters': ['debug_environment'],
            'formatter': 'sql',
            'level': 'DEBUG',
        },
        'info_console_json': {
            'class': 'logging.StreamHandler',
            'filters': ['info_filter'],
            'formatter': 'json_verbose',
            'level': 'INFO',
        },
        'warning_console': {
            'class': 'logging.StreamHandler',
            'filters': ['warning_filter'],
            'formatter': 'json_verbose',
            'level': 'WARNING',
        },
        'error_console': {
            'class': 'logging.StreamHandler',
            'filters': ['error_filter'],
            'formatter': 'json_verbose',
            'level': 'ERROR',
        },
    },
    'formatters': {  # 5.3 格式化
        'sql': {  # SQL
            'format': '【SQL】 {asctime}\n'
                      'duration: {duration}s\n'
                      'sql: {sql}\n'
                      'params: {params}\n',
            'style': '{',
        },
        'json_verbose': {
            'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'filters': {  # 5.4 处理控制
        'debug_environment': {  # DEBUG 环境
            '()': 'django.utils.log.RequireDebugTrue',
        },
        # 'production_environment': {
        #     '()': 'django.utils.log.RequireDebugFalse',
        # },
        'info_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': filter_request('INFO'),
        },
        'warning_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': filter_request('WARNING'),
        },
        'error_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': filter_request('ERROR'),
        },
    },
}

# 6.数据库配置
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
# if DEBUG:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         }
#     }

# 7. 缓存配置
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f'redis://{config("REDIS_HOST")}:{config("REDIS_PORT")}/{config("REDIS_INDEX")}',
        'TIMEOUT': 604800,  # 7 days
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": config("REDIS_PASSWORD")
        }
    }
}

# 7.1 celery 配置
CELERY_BROKER = f'redis://{config("REDIS_HOST")}:{config("REDIS_PORT")}/{config("BROKER_INDEX")}'
CELERY_BACKEND = f'redis://{config("REDIS_HOST")}:{config("REDIS_PORT")}/{config("BACKEND_INDEX")}'
CELERY_IMPORTS = (
    'excel.controller',
    'external.interface',
)

# 8. 邮件配置
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# Default Receiver List
EMAIL_RECEIVER = [config('EMAIL_RECEIVER')]
# Add mail user
# insert into users(email, password) values \
# ('api@emilia.fun', ENCRYPT('1iann', \
# CONCAT('$6$', SUBSTRING(SHA(RAND()), -16))));


# 9. JWT 配置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.DefaultPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'permission.permission.LoginPermission',
    ),
    # disable DRF Browsable Page
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    # 'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# 10. Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 11. I18N 配置
# https://docs.djangoproject.com/en/2.2/topics/i18n/
# LANGUAGE_CODE = 'en-US'
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
# TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 12. Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'

# 13. 应用配置
# 13.1 腾讯短信包
SMS_APPID = config('SMS_APPID')
SMS_APPKEY = config('SMS_APPKEY')
SMS_TEMPLATE_ID = config('SMS_TEMPLATE_ID')

# 13.2 百度人脸
FACE_CLIENT_ID = config('FACE_CLIENT_ID')
FACE_SECRET = config('FACE_SECRET')

# 13.2 百度视觉
VISION_CLIENT_ID = config('VISION_CLIENT_ID')
VISION_SECRET = config('VISION_SECRET')

# 13.3 百度 OCR
OCR_CLIENT_ID = config('OCR_CLIENT_ID')
OCR_SECRET = config('OCR_SECRET')

# 13.4 腾讯 AI
TENCENT_AI_APPID = config('TENCENT_AI_APPID')
TENCENT_AI_APPKEY = config('TENCENT_AI_APPKEY')

# 13.5 腾讯 CoS
COS_BUCKET = config('COS_BUCKET')
COS_ID = config('COS_ID')
COS_KEY = config('COS_KEY')
COS_REGION = config('COS_REGION')
