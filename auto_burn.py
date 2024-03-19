# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : auto_burn.py
# Time   : 2024/3/19 9:09
"""
cron: 0 30 8 * * ?
new Env('BurnHair自动签到');
"""
import os
import time
import requests


def daily_check():
    for i in range(5):
        try:
            print(f'------- 第「{i+1}/5」次尝试 -------')
            cookie = os.environ.get('burn')
            url = 'https://burn.hair/api/user/check_in'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Cookie': cookie
            }
            resp = requests.post(url, headers=headers)
            print(resp.text)
            return
        except Exception as e:
            print(f'{e}')
            time.sleep(10)


if __name__ == '__main__':
    daily_check()
