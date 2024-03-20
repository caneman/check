# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : template.py
# Time   : 2022/10/9 15:42

import re
from copy import copy


def template_factory(template: str, info: dict):
    data = copy(info)
    loop_pattern = re.compile(r'(?s)<loop>(.*?)</loop>')
    body_pattern = re.compile(r'(?s)<body>(.*?)</body>')

    if 'loop' in data.keys():
        loop_list = loop_pattern.findall(template)
        for index, loop in enumerate(loop_list):
            base_loop = '<loop>' + loop + '</loop>'
            replace_loop = ''
            for item in data['loop']:
                replace_loop += loop.format(**item)
            template = template.replace(base_loop, replace_loop)

        del data['loop']
    base_body = body_pattern.findall(template)[0]
    replace_body = base_body.format(**data)
    template = template.replace(base_body, replace_body)
    return template.strip()


EPIC_TEMPLATE = """
<html>
<head>
</head>
<body>
    <div class="wrapper">
        <loop><table class="mainInfo">
            <tr><td>游戏名称：{game_name}</td></tr>
            <tr><td>游戏评分：{game_score}</td></tr>
            <tr><td>截止日期：{game_end_date}</td></tr>
            <tr><td>购买地址：<a href="{game_shop_link}">现在入手</a></td></tr>
        </table>
        <table border="0" align="center" cellpadding="1" cellspacing="0" class="detailInfo">
            <img class="pic" src="cid:{_game_pic_id}">
        </table></loop>
    </div>
</body>
<style type="text/css">
    .wrapper{
        text-align: center;
        width:780px;
        background: #2c323b;
        overflow:hidden;
    }
    .wrapper .mainInfo{
        width: 700px;
        height: 200px;
        margin: 20px auto 10px auto;
        color: #ffffff;
    }
    .mainInfo td{
        text-align: left
    }
    .detailInfo{
        width: 700px;
        margin: 20px auto;
        color: #ffffff;
        padding-bottom: 
    }
    a{
        color: #5ba943;
    }
    .pic{
        width: 700px;

    }
    .detailInfo td{
        height: 35px;
    }
</style>
</html>
"""


if __name__ == '__main__':
    pass
