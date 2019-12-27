#!/bin/bash

# 每次重启运行此处即可
mkdir log -pv

if [[ $DEBUG == 1 ]]; then
  \cp script/debug.env .env -fv
else
  \cp script/product.env .env -fv
fi

. venv/bin/activate
pip install -r requirements.txt
# python manage.py makemigrations
# python manage.py migrate
# watchmedo auto-restart -p './requirements.txt' -- ./reload.sh &

# celery
# 增加 --beat 用于定时调用 celery 任务
# 此处 restart 会等待所有正在运行中的 worker 任务全部结束再运行
# 仍然在队列中等待的会在重启后运行
celery multi restart api --app=api.service --beat --loglevel=info --pidfile=celerybeat.pid --logfile=./log/celery-%n%I.log -c 4
# stop
# celery multi stopwait api -l info --pidfile=celerybeat.pid

# 在 celery 重启完成后再重新加载 gunicorn
# 重启的话脚本会退出
# gunicorn
if [ -f gunicorn.pid ]; then
  # 如果重启时有正在运行的请求则依然是旧的代码的返回
  # 只有所有请求全部结束后才会完全迁移到新的部分
  kill -HUP "$(cat gunicorn.pid)" && exit
fi

# 如果第一次运行会一直在这里
# run.sh
# | - gunicorn
#     |- python
#     |- python
# 如果没有重启（pid 失效）就重新开一个
\rm gunicorn.pid -fv
gunicorn -c gunicorn.py api.wsgi --capture-output --pid gunicorn.pid
