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
import re
import time
import requests
from utils.log import wecom_log
from utils.template import SYMBOL_SUCCESS, SYMBOL_FALSE


def daily_check():
    # 获取有效Cookie
    valid_environ_list = []
    for index in range(100):
        environ_name = 'burn' if index == 0 else f'burn{index}'
        cookie = os.environ.get(environ_name)
        if cookie:
            valid_environ_list.append((environ_name, cookie))

    total = len(valid_environ_list)
    for index, item in enumerate(valid_environ_list):
        environ_name, cookie = item
        msg = ''
        success = False
        for i in range(5):
            try:
                print(f'------- [{index+1}/{total}][{environ_name}]，第「{i+1}/5」次尝试 -------')
                url = 'https://burn.hair/api/user/check_in'
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept': 'application/json, text/plain, */*',
                    'Cookie': cookie
                }
                resp = requests.post(url, headers=headers)
                r_json = resp.json()
                if r_json['success']:
                    count = ''.join(re.findall(r'(\d+)', r_json['message']))
                    msg = f'[BurnHair][{environ_name}]签到成功，获得「{count}」Token'
                    success = True
                elif '已经签到' in r_json['message']:
                    msg = f'[BurnHair][{environ_name}]已签到'
                    success = True
                else:
                    print(f'[BurnHair][{environ_name}]签到失败，{r_json["message"]}')
                    success = False
                break
            except Exception as e:
                print(f'{e}')
                time.sleep(10)

        if success is False:
            msg = f'[BurnHair][{environ_name}]签到失败'
            wecom_log(msg, SYMBOL_FALSE)
        else:
            wecom_log(msg, SYMBOL_SUCCESS)


if __name__ == '__main__':
    daily_check()
