import datetime
import os
import random
import string

import sha3

from . import const


def random_string(rule: str = string.ascii_letters + string.digits, length: int = 16):
    return ''.join(random.sample(rule, length))


def now():
    return datetime.datetime.utcnow()


def read_time(str_time, format='%Y/%m/%d'):
    return datetime.datetime.strptime(str_time, format)


def get_time(utc_time, format='%Y-%m-%d %H:%M:%S', hours=8):
    utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
    tzutc_8 = datetime.timezone(datetime.timedelta(hours=hours))
    local_dt = utc_time.astimezone(tzutc_8).strftime(format)
    return local_dt


def transform_time(str_time, format='%Y/%m/%d', output_format='%Y-%m-%d', hours=0):
    # 时间加上 %H:%M:%S
    return get_time(read_time(str_time, format), output_format, hours)


def list_get(lst, idx, default=None):
    try:
        return lst[idx]
    except IndexError:
        return default


def string_color(msg, color='pink'):
    return f'{const.CONSOLE_COLOR[color]}{msg}{const.CONSOLE_COLOR["end"]}'


def hash(message):
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
        if type(data[i]) == bytes:
            data[i] = '<bytes>'
    return data


def run_shell(command: str):
    result = os.popen(command).read()
    result = [i for i in result.split('\n') if i != '']
    return result
