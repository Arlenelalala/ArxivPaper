import time
import random
from datetime import datetime


def random_sleep(begin=None, end=None):
    if begin is None or begin < 0:
        begin = 0
    if end is None:
        end = 20
    if end >= 1000:
        raise ValueError('%d is too big, expect no more than 1000 seconds!')
    r = random.randint(begin, end)
    for i in range(r):
        time.sleep(1)


def sleep_for(second):
    # print('sleeping...')
    for i in range(second):
        time.sleep(1)
        # print('\r sleep for %d s...' % (second - i))


def timestamp_to_date(timestamp=None, ft=None):
    """
    :type timestamp: int
    """
    if ft is None:
        ft = '%Y-%m-%d'
    if timestamp is None:
        t = time.gmtime()
    else:
        t_str = time.ctime(timestamp)
        t = time.strptime(t_str, '%a %b  %d %H:%M:%S %Y')
    return time.strftime(ft, t)


def timestamp():
    return int(time.time())


def timestamp_str():
    return str(timestamp())


def time_diff(target, ft='%Y-%m-%d'):
    return (datetime.now() - datetime.strptime(target, ft)).days


if __name__ == '__main__':
    s = timestamp_to_date(ft='%Y%m%d')
    print(s)
