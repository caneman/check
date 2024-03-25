# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : auto_reporter.py
# Time   : 2024/3/25 15:05
"""
cron: 0 0 9 * * ?
new Env('日志推送');
"""

import requests
from utils.path import get_env
from utils.text import is_today, today
from utils.log import normal_log
from utils.notice import AbstractPusher
from typing import List


class Reporter(object):

    @classmethod
    def get_task_list(cls):
        client_id, client_secret = get_env('ql_app')
        token_url = f'http://127.0.0.1:5700/open/auth/token?client_id={client_id}&client_secret={client_secret}'
        token_json = requests.get(token_url).json()
        if token_json['code'] != 200:
            normal_log('Token Get Error')
            return []

        token_type = token_json['data']['token_type']
        token = token_json['data']['token']

        task_url = 'http://127.0.0.1:5700/open/crons?searchValue='
        headers = {'Authorization': f'{token_type} {token}'}
        task_json = requests.get(task_url, headers=headers).json()
        if task_json['code'] != 200:
            normal_log('Task Get Error')
            return []

        return task_json['data']['data']

    @classmethod
    def read_log(cls, log_path: str) -> List:
        log_path = '/ql/data/log/' + log_path
        log_list = []
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                log_content = line.strip()
                if log_content:
                    log_list.append(log_content)
        return log_list

    @classmethod
    def push(cls):
        task_list = cls.get_task_list()
        task_must_key = ['isDisabled', 'last_execution_time', 'log_path']

        pusher_list = []
        for pusher in AbstractPusher.__subclasses__():
            pusher_list.append({
                'pusher': pusher,
                'content_list': []
            })

        for item in task_list:
            if sum([1 if k not in item.keys() else 0 for k in task_must_key]) > 0:
                continue

            if str(item['isDisabled']) != '0' or not is_today(item['last_execution_time']):
                continue

            log_list = cls.read_log(item['log_path'])
            for log_content in log_list:
                for pusher in pusher_list:
                    for tag in pusher['pusher'].tags:
                        if log_content.startswith(tag):
                            pusher['content_list'].append(log_content[len(tag):])
                            break

        title = '---- {} ----'.format(today())
        for item in pusher_list:
            pusher = item['pusher']()
            content = '\n'.join(item['content_list'])
            if content:
                pusher.push(title, content)


if __name__ == '__main__':
    Reporter.push()
