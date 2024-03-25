# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : log.py
# Time   : 2024/3/25 15:09

from utils.text import now_time


def log(msg, symbol=''):
    content = f'[{now_time()}]{symbol} - {msg} .'
    print(content)


def wecom_log(msg, symbol=''):
    content = '[企业微信]' + symbol + str(msg).strip()
    print(content)


def normal_log(msg, symbol=''):
    content = f'[{now_time()}]{symbol} - {msg} .'
    print(content)


def pure_log(msg, symbol=''):
    print(f'{symbol}{msg}')


if __name__ == '__main__':
    pass
