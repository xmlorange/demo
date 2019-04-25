# -*- coding: utf-8 -*-

from gevent.pool import Pool
import urllib.request

# 打补丁
import gevent.monkey
gevent.monkey.patch_all()


def spider(url):
    print("Coroutine({0}: spider[{1}] start)".format(gevent.getcurrent().name, url))

    urllib.request.urlopen(url, timeout=2)
    print("Coroutine({0}: spider[{1}] done)".format(gevent.getcurrent().name, url))


if __name__ == '__main__':
    urls = [
        "https://www.baidu.com",
        "https://www.google.com",
        "https://www.taobao.com",
        "https://www.jd.com",
        "https://www.tencent.com",
    ]
    pool = Pool(3)
    for url in urls:
        pool.apply_async(spider, args=(url,))
        pool.join()
