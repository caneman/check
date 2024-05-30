# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : auto_burn.py
# Time   : 2024/3/19 9:09
"""
cron: 0 30 8 * * ?
new Env('BurnHair自动签到');
"""
import re
import json
import time
import requests
from typing import List, Tuple
from utils.log import wecom_log
from utils.path import get_env
from utils.template import SYMBOL_SUCCESS, SYMBOL_FALSE


def get_cookie() -> List[Tuple[str, List[dict]]]:
    valid_environ_list = []
    for index in range(100):
        environ_name = 'burn' if index == 0 else f'burn{index}'
        cookie = get_env(environ_name, split=False)
        if cookie:
            valid_environ_list.append((environ_name, cookie))
    cookie_with_domain_list = []
    for item in valid_environ_list:
        environ_name, cookie_str = item
        cookies = {i.split('=')[0]: '='.join(i.split('=')[1:]) for i in cookie_str.split('; ')}
        cookies_with_domain = [
            {'name': k, 'value': v, 'domain': '.burn.hair'} for k, v in cookies.items()
        ]
        cookie_with_domain_list.append((environ_name, cookies_with_domain))
    return cookie_with_domain_list


def get_flare_url() -> str:
    return get_env('flare_url', split=False)


class BurnHairSpider(object):

    @staticmethod
    def run():
        cookie_list = get_cookie()
        flare_url = get_flare_url()
        if not cookie_list or not flare_url:
            wecom_log('[BurnHair]签到失败，Cookie 或 Flare URL 未配置', SYMBOL_FALSE)
            return

        msg_pattern = re.compile(r'\{.*}')
        total = len(cookie_list)
        for index, item in enumerate(cookie_list):
            success = False
            msg = ''
            for i in range(5):
                try:
                    environ_name, cookies_with_domain = item
                    print(f'------- [{index+1}/{total}][{environ_name}]，第「{i+1}/5」次尝试 -------')
                    payload = {
                        'cmd': 'request.post',
                        'url': 'https://burn.hair/api/user/check_in',
                        'maxTimeout': 60000,
                        'cookies': cookies_with_domain,
                        "postData": "a=b"
                    }
                    response = requests.post(flare_url, json=payload)
                    r_json = response.json()
                    if r_json['status'] == 'ok':
                        item_response = ''.join(msg_pattern.findall(r_json['solution']['response']))
                        item_r_json = json.loads(item_response)
                        if item_r_json['success']:
                            count = ''.join(re.findall(r'(\d+)', item_r_json['message']))
                            msg = f'[BurnHair][{environ_name}]签到成功，获得「{count}」Token'
                            success = True
                        elif '已经签到' in item_r_json['message']:
                            msg = f'[BurnHair][{environ_name}]已签到'
                            success = True
                        else:
                            msg = f'[BurnHair][{environ_name}]签到失败，{item_r_json["message"]}'
                            success = False
                    else:
                        msg = f'[BurnHair][{environ_name}]签到失败', SYMBOL_FALSE
                        success = False
                    break
                except Exception as e:
                    print(f'{e}')
                    time.sleep(10)

            if success is False:
                wecom_log(msg, SYMBOL_FALSE)
            else:
                wecom_log(msg, SYMBOL_SUCCESS)


if __name__ == '__main__':
    BurnHairSpider.run()
