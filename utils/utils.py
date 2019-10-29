import copy
import os

from . import const


def list_get(lst: list, idx: int, default=None):
    try:
        return lst[idx]
    except IndexError:
        return default


def string_color(msg, color='pink'):
    return f'{const.CONSOLE_COLOR[color]}{msg}{const.CONSOLE_COLOR["end"]}'


def protect_dict(data: dict):
    """
    将 bytes 的内容显示为 <bytes>，防止打印不可显示的内容
    """
    if data is None:
        return data

    ret_data = copy.deepcopy(data)
    for i in ret_data:
        if isinstance(ret_data[i], bytes):
            ret_data[i] = '<bytes>'
    return ret_data


def run_shell(command: str):
    result = os.popen(command).read()
    result = [i for i in result.split('\n') if i != '']
    return result
