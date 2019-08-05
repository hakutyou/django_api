import time

from api.service import app


@app.task
# TODO: celery 测试
def add(x, y):
    print('enter call function ...')
    time.sleep(5)
    return x + y
