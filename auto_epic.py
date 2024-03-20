# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : auto_epic.py
# Time   : 2024/3/19 9:17
"""
cron: 0 0 9 ? * 5
new Env(’Epic免费游戏监控');
"""
import time
import requests
from utils.text import timestamp_to_date, today
from utils.notice import WecomPic


def format_date_to_timestamp(date):
    if not date:
        return 0
    date = date.replace('/', '-')
    time_array = time.strptime(date, '%Y-%m-%d')
    timestamp = int(time.mktime(time_array))
    return timestamp


class EpicSpider(object):

    @classmethod
    def get_game_list(cls):
        url = 'https://api.xiaoheihe.cn/mall/add_to_cart/?x_os_type=iOS&platform=epic'
        game_info_json = requests.get(url).json()

        game_info_list = []
        for game in game_info_json['result']['games']:
            game_name = game['name']
            game_amount = game['price']['initial_amount'] if 'price' in game.keys() else '¥--'
            game_score = f'{int(float(game["score"]) * 10)} / 100' if 'score' in game.keys() else '暂无评分'
            game_start_date = today()
            game_end_date = timestamp_to_date(game['end_time'])
            game_pic_link = game['image']
            game_shop_link = 'https://store.epicgames.com/zh-CN/p/' + game['product_name']
            game_info_list.append({
                'game_name': game_name,
                'game_amount': game_amount,
                'game_score': game_score,
                'game_start_date': game_start_date,
                'game_end_date': game_end_date,
                'game_pic_link': game_pic_link,
                'game_shop_link': game_shop_link,
            })
        return game_info_list

    @classmethod
    def run(cls):
        pusher = WecomPic()
        game_info_list = cls.get_game_list()
        for i, game_info in enumerate(game_info_list):
            game_name = game_info['game_name']
            amount = game_info['game_amount']
            score = game_info['game_score']
            start_date = game_info['game_start_date']
            end_date = game_info['game_end_date']
            pic_url = game_info['game_pic_link']
            jump_url = game_info['game_shop_link']
            title = f'{game_name}'
            content = f'游戏评分：{score}\n游戏价格：{amount}\n当前价格：¥0.00\n开始日期：{start_date}\n截止日期：{end_date}'
            pusher.push(title, content, pic_url, jump_url)


if __name__ == '__main__':
    EpicSpider.run()
