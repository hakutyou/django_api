import time
from celery.task import task

from api.service import app
from external.models import CeleryQueueModels


def celery_stage(ic, _type, stage):
    if stage == 0:
        CeleryQueueModels.objects.create(ic=ic, _type=_type, status=stage)
    else:
        celery_queue = CeleryQueueModels.objects.get(ic=ic)
        celery_queue.status = stage
        celery_queue.save(update_fields=['status'])
    return


def celery_catch(func):
    def wrapper(self, ic, _type, *args, **kwargs):
        celery_stage(ic, _type, 1)  # 正在执行或未返回
        ret = func(self, *args, **kwargs)
        celery_stage(ic, _type, 2)  # 执行完成
        return ret

    return wrapper


@app.task(bind=True)
# celery 异步测试
def add(_, x, y):
    print('enter call function ...')
    time.sleep(1)
    return x + y


@task
# celery, beat 定时测试
def run_on_time():
    # print('periodic task test!!!!!')
    return True
