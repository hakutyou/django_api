#!/bin/bash

pip install -r requirements.txt
ps aux | grep gunicorn | grep projectname | awk '{ print $2 }' | xargs kill -HUP
