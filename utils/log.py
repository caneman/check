# -*- coding: utf-8 -*-
# author  : Cane
# QQ      : 54462068

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
