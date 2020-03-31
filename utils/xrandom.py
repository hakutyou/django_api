import random
import string


def random_string(rule: str = string.ascii_letters + string.digits, length: int = 16, exclude=None):
    if exclude:
        rule = set(rule) - set(exclude)
    return ''.join(random.sample(rule, length))


def random_number(range_low, range_height):
    """
    [range_low, range_height] 区间的随机整数
    """
    return random.randint(range_low, range_height)
