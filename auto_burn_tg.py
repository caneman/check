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
import ddddocr
import asyncio
from pathlib import Path
from telethon import TelegramClient, events
from utils.path import get_env
from utils.log import wecom_log, pure_log
from utils.template import SYMBOL_SUCCESS, SYMBOL_FALSE


SESSION_NAME = 'telegram'
CHANNEL_ID = 'burn_hair_bot'
MSG = '/check'
API_ID, API_HASH = get_env('tg_api', split=True)
protocol, ip, port = get_env('tg_proxy', split=True)
PROXY = (protocol, ip, int(port))
CAPTCHA_PATH = Path(__file__).parent / 'captcha/captcha.png'
if not CAPTCHA_PATH.parent.exists():
    CAPTCHA_PATH.parent.mkdir(exist_ok=True)


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH, proxy=PROXY)

    @client.on(events.NewMessage(chats=CHANNEL_ID))
    async def handler(event):
        check_res = event.message.text

        # 是否有点击验证
        if '按钮' not in check_res or '验证码' not in check_res:
            count = ''.join(re.findall(r'(\d+)的额度', check_res))
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
        else:
            # 获取图片
            if event.message.photo:
                await client.download_media(event.message.photo, file=str(CAPTCHA_PATH))

            ocr = ddddocr.DdddOcr(beta=True)
            image = open(CAPTCHA_PATH, "rb").read()
            captcha_code = ocr.classification(image)

            # 获取按钮标题
            if event.message.buttons:
                button_index = -1
                max_match_count = 0
                buttons = event.message.buttons[0]
                for index, button in enumerate(buttons):
                    match_count = 0
                    for i in range(min(len(button.text), len(captcha_code))):
                        if captcha_code[i].lower() == button.text[i].lower():
                            match_count += 1
                    if match_count > max_match_count:
                        button_index = index
                        max_match_count = match_count
                pure_log(f'按钮列表：{[button.text for button in buttons]}，验证码识别结果：{captcha_code}，选择按钮：[{button_index}][{buttons[button_index].text}]')
                await event.click(button_index)
        await client.disconnect()

    await client.start()
    await client.send_message(CHANNEL_ID, MSG)

    await client.run_until_disconnected()


if __name__ == '__main__':
    asyncio.run(main())
