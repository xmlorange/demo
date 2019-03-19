# -*- coding: utf-8 -*-

from app.test.information_summary_filter.memory_filter import MemoryFilter
from app.test.information_summary_filter.redis_filter import RedisFilter
from app.test.information_summary_filter.mysql_filter import MySqlFilter


def test_memory_filter():
    filter = MemoryFilter()

    data = [111, "111", "222", 222, "qwe", "中文"]

    for d in data:
        if filter.is_exists(d):
            print("重复数据 {0}".format(d))
        else:
            filter.save(d)
            print("数据已保存并去重 {0}".format(d))
    print(filter.storage)


def test_redis_filter():
    filter = RedisFilter(redis_key='mykey')

    data = [111, "111", "222", 222, "qwe", "中文"]

    for d in data:
        if filter.is_exists(d):
            print("重复数据 {0}".format(d))
        else:
            filter.save(d)
            print("保存去重的数据 {0}".format(d))
    # print(filter.storage.get("mykey"))


def test_mysql_filter():
    mysql_url = 'mysql+pymysql://root:Bytech123@118.31.115.234:3306/business_uat_2?charset=utf8'
    filter = MySqlFilter(mysql_url=mysql_url)

    data = [111, "111", "222", 222, "qwe", "中文"]

    for d in data:
        if filter.is_exists(d):
            print("重复数据 {0}".format(d))
        else:
            filter.save(d)
            print("保存去重的数据 {0}".format(d))


if __name__ == '__main__':
    # test_redis_filter()
    test_mysql_filter()
