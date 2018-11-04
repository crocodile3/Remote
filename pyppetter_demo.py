# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'Crocodile3'
__mtime__ = '2018/11/4'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import asyncio
import pyppeteer
import os

os.environ['PYPPETEER_CHROMIUM_REVISION'] = '575458'
pyppeteer.DEBUG = True


async def main():
    print("in main ")
    print(os.environ.get('PYPPETEER_CHROMIUM_REVISION'))
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto('http://www.baidu.com')
    
    content = await page.content()
    cookies = await page.cookies()
    # await page.screenshot({'path': 'example.png'})
    await browser.close()
    return {'content': content, 'cookies': cookies}


loop = asyncio.get_event_loop()
task = asyncio.ensure_future(main())
loop.run_until_complete(task)

print(task.result())