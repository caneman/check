# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : check_in.py
# Time   : 2024/3/18 17:57

import os
import requests


def daily_check():
    cookie = os.environ.get('burn')
    url = 'https://burn.hair/api/user/check_in'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Cookie': cookie
    }
    resp = requests.post(url, headers=headers)
    print(resp.text)


if __name__ == '__main__':
    daily_check()
