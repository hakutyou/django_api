import datetime
import random
import string


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
