# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : auto_burn_tg.py
# Time   : 2024/6/6 10:20
"""
cron: 0 30 8 * * ?
new Env('BurnHair TG签到');
"""
import re
import asyncio
from telethon import TelegramClient, events
from utils.path import get_env
from utils.log import wecom_log
from utils.template import SYMBOL_SUCCESS, SYMBOL_FALSE


SESSION_NAME = 'telegram'
CHANNEL_ID = 'burn_hair_bot'
MSG = '/check'
API_ID, API_HASH = get_env('tg_api', split=True)
protocol, ip, port = get_env('tg_proxy', split=True)
PROXY = (protocol, ip, int(port))


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=PROXY)

    @client.on(events.NewMessage(chats=CHANNEL_ID))
    async def handler(event):
        check_res = event.message.text
        count = ''.join(re.findall(r'(\d+)', check_res))
        if count:
            msg = f'[BurnHair]TG签到成功，获得「{count}」Token'
            success = True
        elif '已经签到' in check_res:
            msg = f'[BurnHair]TG已签到'
            success = True
        else:
            msg = f'[BurnHair]TG签到失败，{check_res}'
            success = False

        if success is False:
            wecom_log(msg, SYMBOL_FALSE)
        else:
            wecom_log(msg, SYMBOL_SUCCESS)

        await client.disconnect()

    await client.start()
    await client.send_message(CHANNEL_ID, MSG)

    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
