from external.models import CeleryQueueModels


def celery_stage(ic, _type, stage):
    if stage == 0:
        CeleryQueueModels.objects.create(ic=ic, _type=_type, status=stage)
    else:
        celery_queue = CeleryQueueModels.objects.get(ic=ic)
        celery_queue.status = stage
        celery_queue.save()
    return


def celery_catch(func):
    def wrapper(self, ic, _type, *args, **kwargs):
        celery_stage(ic, _type, 1)
        ret = func(self, *args, **kwargs)
        celery_stage(ic, _type, 2)
        return ret

    return wrapper