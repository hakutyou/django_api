import datetime
import random
import string
import sha3


def random_string(rule: str = string.ascii_letters + string.digits, length: int = 16):
    return ''.join(random.sample(rule, length))


def now():
    return datetime.datetime.utcnow()


def get_time(utc_time, format='%Y-%m-%d %H:%M:%S', hours=8):
    utc_time = utc_time.replace(tzinfo=datetime.timezone.utc)
    tzutc_8 = datetime.timezone(datetime.timedelta(hours=hours))
    local_dt = utc_time.astimezone(tzutc_8).strftime(format)
    return local_dt


def list_get(lst, idx, default=None):
    try:
        return lst[idx]
    except IndexError:
        return default


def print_color(msg, color='pink'):
    color_mapping = {
        'pink': '\033[1;35m',
        'origin': '\033[0m',
    }
    default_color = color_mapping['pink']
    origin_color = color_mapping['origin']
    print(f'{color_mapping.get(color, default_color)}{msg}{origin_color}')


def hash(message):
    """
    该项目使用的信息摘要算法
    """
    k = sha3.keccak_224()
    k.update(bytes(message, encoding='utf-8'))
    return k.hexdigest()
