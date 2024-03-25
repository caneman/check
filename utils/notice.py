# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : notice.py
# Time   : 2024/3/25 15:10

import json
import requests
from abc import ABCMeta, abstractmethod
from utils.path import get_env


class AbstractPusher(metaclass=ABCMeta):

    tags = []

    def __init__(self, environ_name: str = '') -> None:
        self.environ_name = environ_name

    @abstractmethod
    def push(self, *args, **kwargs):
        pass


class Wecom(AbstractPusher):

    tags = ['[企业微信]']

    def __init__(self, environ_name: str = 'wecom') -> None:
        super().__init__(environ_name)

    def post_msg(self, msg: str, to_user: str) -> None:
        _id, secret, default_to_user, agent_id = get_env(self.environ_name)
        wecom_proxy = get_env('wecom_proxy')
        wecom_host = wecom_proxy if wecom_proxy else 'https://qyapi.weixin.qq.com'
        wecom_host = wecom_host[:-1] if wecom_host.endswith('/') else wecom_host
        token_url = f'{wecom_host}/cgi-bin/gettoken?corpid={_id}&corpsecret={secret}'
        token = requests.get(token_url).json()['access_token']
        url = f'{wecom_host}/cgi-bin/message/send?access_token={token}&debug=1'
        to_user = to_user if to_user else default_to_user
        data = {
            'touser': to_user,
            'msgtype': 'text',
            'agentid': agent_id,
            'text': {
                'content': msg
            }

        }
        requests.post(url, data=json.dumps(data))

    def push(self, title: str, content: str, to_user: str = '') -> None:
        msg = '{}\n{}'.format(title, content).strip()
        self.post_msg(msg, to_user)


class WecomPic(AbstractPusher):

    tags = ['[企业微信图片]']

    def __init__(self, environ_name: str = 'wecom') -> None:
        super().__init__(environ_name)

    def post_msg(self, title, content, pic_url, jump_url):
        _id, secret, to_user, agent_id = get_env(self.environ_name)
        wecom_proxy = get_env('wecom_proxy')
        wecom_host = wecom_proxy if wecom_proxy else 'https://qyapi.weixin.qq.com'
        wecom_host = wecom_host[:-1] if wecom_host.endswith('/') else wecom_host
        token_url = f'{wecom_host}/cgi-bin/gettoken?corpid={_id}&corpsecret={secret}'
        token_resp = requests.get(token_url)
        token = json.loads(token_resp.text)['access_token']
        url = f'{wecom_host}/cgi-bin/message/send?access_token={token}&debug=1'
        data = {
            'touser': str(to_user),
            'msgtype': 'news',
            'agentid': str(agent_id),
            'news': {'articles': [
                {
                    'title': title,
                    'description': content,
                    'url': jump_url,
                    'picurl': pic_url
                }]
            }
        }
        requests.post(url, data=json.dumps(data))

    def push(self, title, content, pic_url='', jump_url=''):
        self.post_msg(title, content, pic_url, jump_url)


class WecomRobot(AbstractPusher):

    tags = ['[企业微信机器人]']

    def __init__(self, environ_name: str = 'wecom_robot') -> None:
        super().__init__(environ_name)

    def post_msg(self, content: str) -> None:
        url = get_env(self.environ_name)
        data = {
            'msgtype': 'text',
            'text': {'content': content}
        }
        requests.post(url, data=json.dumps(data))

    def push(self, title: str, content: str) -> None:
        msg = '{}\n{}'.format(title, content).strip()
        self.post_msg(msg)


if __name__ == '__main__':
    pass
