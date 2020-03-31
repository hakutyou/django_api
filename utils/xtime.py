# 时间相关
# 时区使用 datetime.timezone.utc ，只有需要打印为 str (strtime) 时候设置时区，默认为 utc+8

import datetime

from django.utils import timezone


def now() -> datetime.datetime:
    return timezone.now()


def from_timestamp_to_strtime(timestamp, time_format='%Y-%m-%d %H:%M:%S', hours: int = 8) -> str:
    return to_strtime(from_timestamp(timestamp), time_format, hours)


def from_strtime_to_timestamp(str_time: str, time_format='%Y-%m-%d %H:%M:%S', hours: int = 8) -> float:
    return to_timestamp(from_strtime(str_time, time_format, hours))


def to_date(utc_time: datetime.datetime) -> datetime.date:
    """
    datetime.datetime 转 date （丢失时间信息）
    """
    return utc_time.date()


def to_timestamp(utc_time: datetime.datetime) -> float:
    """
    datetime.datetime 转 1970 年至今的秒数
    """
    return utc_time.timestamp()


def from_timestamp(timestamp) -> datetime.datetime:
    """
    1970 年至今的秒数转 datetime.datetime
    timestamp 为 float 或可以转为 float() 的类型
    """
    return datetime.datetime.fromtimestamp(float(timestamp)).astimezone(datetime.timezone.utc)


def to_strtime(utc_time: datetime.datetime, time_format='%Y-%m-%d %H:%M:%S', hours: int = 8) -> str:
    """
    从 datetime 转 strtime
    """
    _timezone = datetime.timezone(datetime.timedelta(hours=hours))
    return utc_time.astimezone(_timezone).strftime(time_format)


def from_strtime(str_time: str, time_format='%Y-%m-%d %H:%M:%S', hours: int = 8):
    """
    从 strtime 转 datetime
    """
    _timezone = datetime.timezone(datetime.timedelta(hours=hours))
    _time_withtz = datetime.datetime.strptime(str_time, time_format).replace(tzinfo=_timezone)
    return _time_withtz.astimezone(datetime.timezone.utc)


def transform_strtime(str_time: str, time_format='%Y%m%d%H%M%S', output_format='%Y-%m-%d %H:%M:%S',
                      hours: int = 8) -> str:
    return to_strtime(from_strtime(str_time, time_format), output_format, hours)


def get_days_between(start_date: datetime.datetime, end_date: datetime.datetime) -> int:
    """
    获取两个日期之间相隔多少天
    datetime 类型加上 .date 获取日期
    """
    return (end_date - start_date).days


def get_weeks_between(start_date: datetime.datetime, end_date: datetime.datetime, first_day: bool = True) -> int:
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
