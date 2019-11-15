import copy
import os
from typing import Union

from . import const


def list_get(lst: list, idx: int, default=None):
    try:
        return lst[idx]
    except IndexError:
        return default


def string_color(msg, color='pink'):
    return f'{const.CONSOLE_COLOR[color]}{msg}{const.CONSOLE_COLOR["end"]}'


def protect_dict_or_list(data: Union[dict, list]):
    """
    将 bytes 的内容显示为 <bytes>，防止打印不可显示的内容
    """
    if data is None:
        return data

    if isinstance(data, dict):
        ret_data = copy.deepcopy(data)
        for i in ret_data:
            if isinstance(ret_data[i], bytes):
                ret_data[i] = '<bytes>'
    elif isinstance(data, list):
        ret_data = list(map(lambda x: '<bytes>' if isinstance(x, bytes) else x, data))
    else:
        ret_data = copy.deepcopy(data)
    return ret_data


def run_shell(command: str):
    result = os.popen(command).read()
    result = [i for i in result.split('\n') if i != '']
    return result
