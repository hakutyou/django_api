import datetime
import os
import random
import string

import sha3
from django.utils import timezone

from . import const


def random_string(rule: str = string.ascii_letters + string.digits, length: int = 16):
    return ''.join(random.sample(rule, length))


def now():
    return timezone.now()


def read_time(str_time, time_format='%Y/%m/%d'):
    return datetime.datetime.strptime(str_time, time_format)


def get_time(utc_time, time_format='%Y-%m-%d %H:%M:%S', hours=8):
    utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
    tzutc_8 = datetime.timezone(datetime.timedelta(hours=hours))
    local_dt = utc_time.astimezone(tzutc_8).strftime(time_format)
    return local_dt


def transform_time(str_time, time_format='%Y/%m/%d', output_format='%Y-%m-%d', hours=0):
    # 时间加上 %H:%M:%S
    return get_time(read_time(str_time, time_format), output_format, hours)


def list_get(lst: list, idx: int, default=None):
    try:
        return lst[idx]
    except IndexError:
        return default


def string_color(msg, color='pink'):
    return f'{const.CONSOLE_COLOR[color]}{msg}{const.CONSOLE_COLOR["end"]}'


def message_digest(message: str) -> str:
    """
    该项目使用的信息摘要算法
    """
    k = sha3.keccak_224()
    k.update(bytes(message, encoding='utf-8'))
    return k.hexdigest()


def protect_dict(data: dict):
    if data is None:
        return data

    for i in data:
        if isinstance(data[i], bytes):
            data[i] = '<bytes>'
    return data


def run_shell(command: str):
    result = os.popen(command).read()
    result = [i for i in result.split('\n') if i != '']
    return result
