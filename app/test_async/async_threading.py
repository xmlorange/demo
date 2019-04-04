# -*- coding: utf-8 -*-

import threading
import time
import asyncio


def now(): return time.time()


async def task_func():
    print("task_func: {0}".format(threading.current_thread()))
    print("task_func start")
    await asyncio.sleep(3)
    print("task_func done")


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


def callback(second):
    print("callback: {0}".format(threading.current_thread()))
    time.sleep(second)


start = now()
new_loop = asyncio.new_event_loop()

# 子线程中启动事件循环
t = threading.Thread(target=start_loop, args=(new_loop,))
t.start()

# 向子线程中运行的事件循环, 注册事件
asyncio.run_coroutine_threadsafe(task_func(), new_loop)

# call_soon, 立刻安排回调函数并执行
new_loop.call_soon(callback, 1)
# 同call_soon, 但它是线程安全的, 避免线程资源竞争
new_loop.call_soon_threadsafe(callback, 2)

# 主线程后面可以继续执行其他代码
# 最后时候挂起，等待子线程的结束
print("主线程: 可以做其他事情")
print("耗时: {0}".format(now() - start))
