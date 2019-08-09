#!/bin/bash

cp script/product.env .env
pip install -r requirements.txt
# python manage.py makemigrations
# python manage.py migrate
pgrep gunicorn | xargs kill -HUP
