# -*- coding: utf-8 -*-

import asyncio
import time


# now = lambda: time.time()
def now(): return time.time()


# callback: 事件处理器函数
def event_handler(future):
    if future:
        print("购买{0}成功,可以开始玩游戏".format(future.result()))
    else:
        print("购买失败!")


# 1.定义协程函数: 购买事件
async def buy(item):
    return item


start = now()
# 2.调用协程函数,获取协程对象
coroutine = buy("电脑")
# 3.获取默认的事件循环对象
loop = asyncio.get_event_loop()
# 4.根据协程对象创建task对象: 注册事件event 有3种方法构建task对象
task = loop.create_task(coroutine)
# task = asyncio.ensure_future(coroutine)
# task = asyncio.Task(coroutine)

# 5.设置回调函数,也就是 event_handler
task.add_done_callback(event_handler)
print(task)

# 6.启动事件循环, 一旦启动 事件就会被监听或者调用
loop.run_until_complete(task)
print(task)
print("耗时{0}".format(now() - start))


if __name__ == '__main__':
    pass
