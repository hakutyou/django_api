#!/bin/sh

pip install -r requirements.txt
cp script/product.env .env
gunicorn -c gunicorn.py api.wsgi --capture-output
