# -*- coding: utf-8 -*-
import gevent
import urllib.request

# 打补丁
from gevent import monkey

monkey.patch_all()


def test1():
    print("test1 start")
    urllib.request.urlopen("http://www.baidu.com")
    print("test1 done")


def test2():
    print("test2 start")
    urllib.request.urlopen("http://www.baidu.com")
    print("test2 done")


if __name__ == '__main__':

    gevent_greenlet1 = gevent.spawn(test1)
    gevent_greenlet2 = gevent.spawn(test2)

    gevent.joinall([
        gevent_greenlet1,
        gevent_greenlet2,
    ])
