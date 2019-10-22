import os
import random
import string

from . import const


def random_string(rule: str = string.ascii_letters + string.digits, length: int = 16):
    return ''.join(random.sample(rule, length))


def list_get(lst: list, idx: int, default=None):
    try:
        return lst[idx]
    except IndexError:
        return default


def string_color(msg, color='pink'):
    return f'{const.CONSOLE_COLOR[color]}{msg}{const.CONSOLE_COLOR["end"]}'


def protect_dict(data: dict):
    """
    将 bytes 的内容显示为 <bytes>，防止打印过长的内容
    """
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
