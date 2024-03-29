# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : auto_hifini.py
# Time   : 2024/3/27 16:42
"""
cron: 0 30 8 * * ?
new Env('Hifini自动签到');
"""

import re
import requests
from utils.path import get_env
from utils.log import wecom_log, pure_log
from utils.template import SYMBOL_FALSE, SYMBOL_SUCCESS


class HifiniSpider(object):

    def __init__(self):
        self.cookie = get_env('hifini', split=False)
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'

    def get_sign(self) -> str:
        url = 'https://hifini.com/my.htm'
        headers = {'User-Agent': self.ua, 'Cookie': self.cookie}
        resp = requests.get(url, headers=headers)
        pattern = re.compile(r'var sign = "(.*?)";')
        sign = ''.join(pattern.findall(resp.text))
        return sign

    def run(self):
        sign = self.get_sign()
        if not sign:
            pure_log('获取签名失败, 请检查 Cookie 是否失效')
            wecom_log('[Hifini]签到失败，请检查 Cookie 是否失效', SYMBOL_FALSE)
            return
        else:
            pure_log(f'获取签名成功: {sign}')

        url = 'https://hifini.com/sg_sign.htm'
        data = {'sign': sign}
        headers = {
            'User-Agent': self.ua,
            'Cookie': self.cookie,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        resp = requests.post(url, headers=headers, data=data)
        if '已经签过' in resp.text:
            wecom_log('[Hifini]签到成功', SYMBOL_SUCCESS)
        elif '成功签到' in resp.text:
            rank_pattern = re.compile(r'成功签到！今日排名(\d+)，总奖励\d+金币！')
            coin_pattern = re.compile(r'成功签到！今日排名\d+，总奖励(\d+)金币！')
            rank = ''.join(rank_pattern.findall(resp.text))
            coin = ''.join(coin_pattern.findall(resp.text))
            if rank and coin:
                wecom_log(f'[Hifini]签到成功，今日排名: {rank}，获得金币: {coin}', SYMBOL_SUCCESS)
            else:
                wecom_log(f'[Hifini]签到成功', SYMBOL_SUCCESS)
        else:
            wecom_log('[Hifini]签到失败', SYMBOL_FALSE)


if __name__ == '__main__':
    spider = HifiniSpider()
    spider.run()
