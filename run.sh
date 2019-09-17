#!/bin/sh

pip install -r requirements.txt
mkdir log -p
cp script/product.env .env

watchmedo auto-restart -p './requirements.txt' -- ./install.sh &
gunicorn -c gunicorn.py api.wsgi --capture-output

