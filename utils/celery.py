from celery.result import AsyncResult
from celery.task import task

from external.models import CeleryQueueModels
from utils import xtime, xrandom


def celery_stage(ic, _type, stage):
    if stage == 0:
        CeleryQueueModels.objects.create(ic=ic, _type=_type, status=stage)
    else:
        celery_queue = CeleryQueueModels.objects.get(ic=ic)
        celery_queue.status = stage
        celery_queue.save(update_fields=['status'])
    return


def append_celery(_type, func, *args, **kwargs):
    ic = xtime.to_strtime(xtime.now(), time_format='%Y%m%d%H%M%S') + xrandom.random_string(length=6)
    celery_stage(ic, _type, 0)
    celery_id = func.delay(ic, _type, *args, **kwargs)
    celery_queue = CeleryQueueModels.objects.get(ic=ic)
    celery_queue.celery_id = celery_id
    celery_queue.save(update_fields=['celery_id'])
    return ic


def celery_check(ic):
    celery_queue = CeleryQueueModels.objects.get(ic=ic)
    status = celery_queue.status
    if status != 2:
        return status, None
    result = AsyncResult(celery_queue.celery_id)
    return status, result.get()


def celery_catch(func):
    def wrapper(self, ic, _type, *args, **kwargs):
        celery_stage(ic, _type, 1)  # 正在执行或未返回
        try:
            ret = func(self, *args, **kwargs)
        except Exception as e:
            celery_stage(ic, _type, -1)  # 执行失败
            raise e
        celery_stage(ic, _type, 2)  # 执行完成
        return ret

    return wrapper


@task
# celery, beat 定时测试
def run_on_time():
    print('periodic task test!!!!!')
    return True
