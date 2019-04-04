# -*- coding: utf-8 -*-

import asyncio
import time


def now(): return time.time()


async def task0():
    await asyncio.sleep(1)
    print("task0 done")
    return "task0 complete"


async def task1():
    await asyncio.sleep(1)
    print("task1 done")
    return "task1 complete"


async def task2():
    await asyncio.sleep(1)
    print("task2 done")
    return "task2 complete"


async def task3():
    await asyncio.sleep(1)
    print("task2 done")
    return "task3 complete"


async def main():
    tasks = [task0(), task1(), task2(), task3()]

    # 有三种方式进行协程组合嵌套
    # 1. asyncio.wait()
    dones, pendings = await asyncio.wait(tasks)  # dones 对应task的返回值, pendings 对应的task的状态
    for task in dones:
        print(task.result())

    # 2. asyncio.as_completed()
    for task in asyncio.as_completed(tasks):
        result = await task
        print(result)

    # 3. asncio.gather()
    result = await asyncio.gather(*tasks)
    print(result)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
