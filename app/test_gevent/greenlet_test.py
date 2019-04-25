# -*- coding: utf-8 -*-


def test_greenlet():
    from greenlet import greenlet

    def test1():
        print("test1 start")
        # 执行协程2: 在协程1内部直接switch切换到协程2执行
        corotine2.switch()
        print("test1 done")
        # 执行协程2: 在协程1内部直接switch切换到协程2执行
        corotine2.switch()

    def test2():
        print("test2 start")
        # 执行协程1: 在协程2内部直接switch切换到协程1执行
        corotine1.switch()
        print("test2 done")

    corotine1 = greenlet(test1)
    corotine2 = greenlet(test2)
    # 执行协程1
    # 主协程
    corotine1.switch()


def test_yield():

    def test1():
        print("test1 start")
        yield
        print("test1 done")

    def test2():
        print("test2 start")
        yield
        print("test2 done")

    corotine1 = test1()
    corotine2 = test2()

    # 执行协程1
    next(corotine1)
    # 执行协程2
    next(corotine2)
    try:
        next(corotine1)
    # 调用生成器时，当没有下一个next()调用时会抛出异常 使用StopIteration捕获
    except StopIteration:
        pass

    try:
        next(corotine2)
    except StopIteration:
        pass


if __name__ == '__main__':
    test_greenlet()
    print("*******************")
    test_yield()
