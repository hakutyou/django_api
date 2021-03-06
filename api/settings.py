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
    'rest_framework_swagger',
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
    # CSRF 开关
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'log_request_id.middleware.RequestIDMiddleware',
    'api.middleware.EnhanceMiddleware',
]

# 3. 跨域访问配置
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_REGEX_WHITELIST = [
    'https?://emilia.fun',
    'https?://hakutyou.xyz',
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
# 跨项目调用接口使用相同的 request_id
LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'
OUTGOING_REQUEST_ID_HEADER = 'X-Request-Id'
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True
REQUEST_ID_RESPONSE_HEADER = 'RESPONSE_HEADER_NAME'
LOG_REQUESTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # True 表示禁用默认的日志，例如 404 提示
    'loggers': {  # 5.1 总览
        'django.db.backends': {
            'handlers': ['sql'],
            'propagate': False,
            'level': 'DEBUG'
        },
        'api': {  # 项目内的 logger.info
            'handlers': ['json_console', 'json_file'],
            'propagate': False,
            'level': 'DEBUG',
        }
    },
    'handlers': {  # 5.2 处理信息
        'sql': {
            # 输出到 stderr
            'class': 'logging.StreamHandler',
            'filters': ['debug_environment', 'request_id'],
            'formatter': 'sql',
            'level': 'DEBUG',
        },
        'json_console': {
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'json_pretty',
            'level': 'DEBUG',
        },
        'json_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filters': ['request_id'],
            'formatter': 'json_verbose',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
            'filename': 'log/info.log',
            'level': 'DEBUG',
        }
    },
    'formatters': {  # 5.3 格式化
        'sql': {  # SQL
            'format': '【SQL】 {asctime}\n'
                      'rid: {request_id}\n'
                      'duration: {duration}s\n'
                      'sql: {sql}\n'
                      'params: {params}\n',
            'style': '{'
        },
        'json_pretty': {
            '()': 'api.logformatter.JsonPrettyFormatter',
        },
        'json_verbose': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'filters': {  # 5.4 处理控制
        'debug_environment': {  # DEBUG 环境
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'production_environment': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        },
    },
}

# 6.数据库配置
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        # mysql 才需要 utf8mb4
        # 'OPTIONS': {
        #     'charset': 'utf8mb4',
        # },
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

# 7. celery, beat 配置
CELERY_BROKER = f'redis://:{config("REDIS_PASSWORD")}@{config("REDIS_HOST")}' \
                f':{config("REDIS_PORT")}/{config("BROKER_INDEX")}'
CELERY_BACKEND = f'redis://:{config("REDIS_PASSWORD")}@{config("REDIS_HOST")}' \
                 f':{config("REDIS_PORT")}/{config("BACKEND_INDEX")}'
# 其他参数配置移动到 celery.py


# 8. 邮件配置
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=True, cast=bool)
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
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
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

# 文档配置
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        "basic": {
            'type': 'basic'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用 restframework 自带的.
    'LOGIN_URL': '/api/account/login/',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 接口文档中方法列表以首字母升序排列
    # 'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
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

# 13.6 腾讯 SCF
TENCENT_SCF_SECRET_ID = config('TENCENT_SCF_SECRET_ID')
TENCENT_SCF_SECRET_KEY = config('TENCENT_SCF_SECRET_KEY')
