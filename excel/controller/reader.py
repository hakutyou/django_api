import time

from api.service import app


@app.task(bind=True)
# TODO: celery 测试
def add(self, x, y):
    print('enter call function ...')
    time.sleep(5)
    return x + y
