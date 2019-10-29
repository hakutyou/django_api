# 时间相关

import datetime

import time
from django.utils import timezone


def now():
    return timezone.now()


def read_time(str_time, time_format='%Y/%m/%d'):
    return datetime.datetime.strptime(str_time, time_format)


def read_1970_time(str_second, time_format='%Y-%m-%d %H:%M:%S') -> str:
    """
    1970 年至今的秒数转时间
    """
    time_array = time.localtime(float(str_second))
    return time.strftime(time_format, time_array)


def get_time(utc_time, time_format='%Y-%m-%d %H:%M:%S', hours=8):
    utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
    tzutc_8 = datetime.timezone(datetime.timedelta(hours=hours))
    return utc_time.astimezone(tzutc_8).strftime(time_format)


def transform_time(str_time, time_format='%Y/%m/%d', output_format='%Y-%m-%d', hours=0):
    # 时间加上 %H:%M:%S
    return get_time(read_time(str_time, time_format), output_format, hours)


def get_days_between(start_date, end_date):
    """
    获取两个日期之间相隔多少天
    datetime 类型加上 .date 获取日期
    """
    return (end_date - start_date).days


def get_weeks_between(start_date, end_date, first_day=True):
    """
    获取两个日期之间相隔多少周
    first_day = 0 到 6 表示周 n 为一周第一天
    datetime 类型加上 .date 获取日期
    """
    # .weekday 的 0-6 代表周一到周日
    start_weekday = (start_date.weekday() + 1 - first_day) % 7
    end_weekday = (end_date.weekday() + 1 - first_day) % 7

    week_start = start_date - datetime.timedelta(days=start_weekday)
    week_end = end_date - datetime.timedelta(days=end_weekday)
    return (week_end - week_start).days // 7
