# -*- coding: utf-8 -*-
# author  : Cane
# QQ      : 54462068

import json
import requests
from abc import ABCMeta, abstractmethod
from utils.path import get_env


class AbstractPusher(metaclass=ABCMeta):

    tags = []
    default_config = ''

    def __init__(self, config: str = '') -> None:
        self.config = config if config else self.default_config

    @abstractmethod
    def push(self, *args, **kwargs):
        pass


class Wecom(AbstractPusher):

    tags = ['[企业微信]']
    default_config = 'wecom'

    def __init__(self, config: str = '') -> None:
        super().__init__(config)

    def post_msg(self, msg: str, to_user: str) -> None:
        _id, secret, default_to_user, agent_id = get_env(self.config)
        token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(_id, secret)
        token = requests.get(token_url).json()['access_token']

        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}&debug=1'.format(token)
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
    default_config = 'wecom'

    def __init__(self, config: str = '') -> None:
        super().__init__(config)

    def post_msg(self, title, content, pic_url, jump_url):
        _id, secret, to_user, agent_id = get_env(self.config)
        token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(_id, secret)
        token_resp = requests.get(token_url)
        token = json.loads(token_resp.text)['access_token']

        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}&debug=1'.format(token)
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
    default_config = 'wecom_robot'

    def __init__(self, config: str = '') -> None:
        super().__init__(config)

    def post_msg(self, content: str) -> None:
        url = get_env(self.config)
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
