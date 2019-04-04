# -*- coding: utf-8 -*-

"""task 任务取消"""

import asyncio
import time


def now(): return time.time()


# 1. 定义协程函数
async def task1():
    print("task1 start")
    await asyncio.sleep(5)
    print("task1 done")


async def task2():
    print("task1 start")
    await asyncio.sleep(1)
    print("task1 done")


def callback(future):
    loop.stop()


start = now()

loop = asyncio.get_event_loop()

task1 = asyncio.Task(task1())
task2 = asyncio.Task(task2())
task2.add_done_callback(callback)

loop.run_forever()
