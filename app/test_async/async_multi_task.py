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
    await asyncio.sleep(1)  # await 交出代码执行控制权(类似于 yield from), 同时await 只能是三种对象中的一种: 协程对象 Task对象 future对象
    return item


start = now()


# 2.获取默认的事件循环对象
loop = asyncio.get_event_loop()

tasks = list()
for i in ["电脑", "手机", "平板", "游戏机", "笔记本电脑", "爬虫书籍", "空调"]:
    # 3.根据协程对象创建task对象: 注册事件event 有3种方法构建task对象
    task = asyncio.ensure_future(buy(i))

    # 4.设置回调函数,也就是 event_handler
    task.add_done_callback(event_handler)
    tasks.append(task)

# 5.启动事件循环, 一旦启动 事件就会被监听或者调用
# run_until_complete() 只能传入三种类型的对象 : 协程对象 Task对象 future对象
loop.run_until_complete(asyncio.wait(tasks))    # asyncio.wait(tasks) 把列表对象转化成 future对象
# print(tasks)
print("耗时{0}".format(now() - start))


if __name__ == '__main__':
    pass
