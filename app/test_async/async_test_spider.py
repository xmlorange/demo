# -*- coding: utf-8 -*-

import time
import asyncio
import requests


def now(): return time.time()


start = now()


async def task(loop, url):
    future = loop.run_in_executor(None, requests.get, url)
    response = await future
    return response.text


async def main():
    loop = asyncio.get_event_loop()

    tasks = list()

    tasks.append(task(loop, "http://www.baidu.com"))
    tasks.append(task(loop, "http://www.taobao.com"))

    result = await asyncio.gather(*tasks)
    print(result)

new_loop = asyncio.get_event_loop()
new_loop.run_until_complete(main())
print(now() - start)
