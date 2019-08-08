#!/bin/sh

pip install -r requirements.txt
cp script/product.env .env

watchmedo auto-restart -p './requirements.txt' -- pip install -r requirements.txt && \
  ps aux |grep gunicorn |grep projectname | awk '{ print $2 }' |xargs kill -HUP &

gunicorn -c gunicorn.py api.wsgi --capture-output


