#!/bin/sh

# 修正 mongolog 的 bug
sed -i 's/,serverSelectionTimeoutMS=5//' `find venv/lib/python3.6/site-packages/mongolog -type f`