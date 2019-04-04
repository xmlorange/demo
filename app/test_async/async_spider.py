# -*- coding: utf-8 -*-

import time
import aiohttp
import asyncio
import requests


def now(): return time.time()


start = now()
"""方案一"""

#
# async def fetch(session, url):
#     async with session.get(url) as response:
#         return await response.text()
#
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         html = await fetch(session, "http://www.baidu.com")
#         print(html)
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

"""方案二"""


async def main():
    new_loop = asyncio.get_event_loop()
    future1 = new_loop.run_in_executor(None, requests.get, 'http://www.baidu.com')
    future2 = new_loop.run_in_executor(None, requests.get, 'http://www.taobao.com')

    response1 = await future1
    response2 = await future2
    print(response1.text)
    print(response2.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print(now() - start)