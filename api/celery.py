import datetime

# 7.1 celery 配置
CELERY_IMPORTS = (
    # 需要 celery 的文件列表
    'utils.celery',
)

# 7.2 beat 配置
CELERYBEAT_SCHEDULE = {
    # 'run_on_time_per_10_second': {
    #     'task': 'utils.celery.run_on_time',
    #     # Executes every Monday morning at 7:30 a.m.
    #     # 'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     # 每 10 秒调用一次, 第一次调用在运行 10 秒之后
    #     'schedule': datetime.timedelta(seconds=10),
    #     'args': (),
    # },
}
