# -*- coding: utf-8 -*-
import multiprocessing

cpu_count = multiprocessing.cpu_count()

# workers = 4 * cpu_count
threads = 4 * cpu_count
#worker_class = 'gevent'
worker_class = 'tornado'

reload = True

# if is_production:
#    bind = "0.0.0.0:8001"
#    raw_env = ['DJANGO_SETTINGS_MODULE=mighty_cashier.online']
# else:
# bind = "127.0.0.1:8000"
bind = 'unix:/var/run/sock/django.sock'
user = None
group = None
umask = 0x0  # umask 为与运算

raw_env = ['PRODUCT=1;DJANGO_SETTINGS_MODULE=api.settings']

loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = '/var/log/gunicorn_access.log'
errorlog = '/var/log/gunicorn_error.log'
