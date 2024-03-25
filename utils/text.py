# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : text.py
# Time   : 2024/3/25 15:11

import time


def now_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def today():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def last_day():
    return time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))


def get_timestamp(ms=False):
    if ms:
        return int(time.time() * 1000)
    else:
        return int(time.time())


def timestamp_to_date(ts):
    ts = int(ts)
    return time.strftime('%Y-%m-%d', time.localtime(ts))


def is_today(timestamp):
    if str(today()) == time.strftime('%Y-%m-%d', time.localtime(int(timestamp))):
        return True
    else:
        return False


if __name__ == '__main__':
    pass
