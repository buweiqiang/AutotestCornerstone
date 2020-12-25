#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File : pyppeteer_demo.py 
@Contact : buweiqiang@civaonline.cn
@MTime : 2020-12-25 15:30 
@Author: buweiqiang
@Version: 1.0
@Desciption: None
'''

# 最好指定一下自己浏览器的位置，如果不指定会自动下载，太慢了...
executable_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

import asyncio
from pyppeteer import launch
from pyppeteer.browser import Browser
import os


async def capture_web(browser: Browser, url):
    page = await browser.newPage()
    await page.goto(url)
    page_title = await page.title()
    print(page_title)
    if not os.path.exists('./pyppeteer/'):
        os.mkdir('./pyppeteer/')
    await page.screenshot(path=f'./pyppeteer/{page_title}.png')


urls = ['http://www.baidu.com', 'https://www.iana.org/domains/reserved', 'http://www.163.com']


async def test():
    browser = await launch(executablePath=executable_path, defaultViewport={'width': 1024, 'height': 768})
    await asyncio.gather(*(capture_web(browser, url) for url in urls))
    await browser.close()


asyncio.run(test())
