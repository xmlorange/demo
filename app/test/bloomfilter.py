# -*- coding: utf-8 -*-
# 布隆过滤器 redis版本
import hashlib

import redis
import six

# 1 多个hash函数的封装和求值
# 2 hash表实现 和实现对应的映射和判断


class MultipleHash(object):
    """根据提供的原始数据, 和预定义的多个salt, 生成多个hash函数"""

    def __init__(self, salts, hash_func_name="md5"):
        self.hash_func = getattr(hashlib, hash_func_name)
        self.salts = salts
        if len(self.salts) < 3:
            raise Exception("please provide at least 3 salt")

    def _safe_data(self, data):
        """
        处理字符串
        python2 str === python3 bytes
        python2 unicode === python3 str
        :param data: 原始数据
        :return: 二进制类型的数据
        """
        if six.PY3:
            if isinstance(data, bytes):
                return data
            elif isinstance(data, str):
                return data.encode()
            elif isinstance(data, int):
                return str(data).encode()
            else:
                raise Exception("please provide string")
        else:
            if isinstance(data, str):
                return data
            elif isinstance(data, unicode):
                return data.encode()
            else:
                raise Exception("please provide string")

    def get_hash_values(self, data):
        """根据提供的原始数据, 返回多个hash函数值"""
        hash_values = list()
        for i in self.salts:
            hash_obj = self.hash_func()
            hash_obj.update(self._safe_data(data))
            hash_obj.update(self._safe_data(i))
            hash_values.append(int(hash_obj.hexdigest(), 16))
        return hash_values


class BloomFilter(object):
    """"""
    def __init__(self, salts, redis_host="localhost", redis_port=6379, redis_db=0, redis_key="bloomfilter"):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_key = redis_key
        self.client = self._get_redis_client()

        self.multiple_hash = MultipleHash(salts)

    def _get_redis_client(self):
        pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        client = redis.StrictRedis(connection_pool=pool)
        return client

    def save(self, data):
        hash_values = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            self.client.setbit(self.redis_key, offset, 1)
        return True

    def is_exists(self, data):
        hash_values = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            v = self.client.getbit(self.redis_key, offset)
            if v == 0:
                return False
            return True

    @staticmethod
    def _get_offset(hash_value):
        """2**8 = 256  2**20 = 1024 * 1024"""
        return hash_value % (2 ** 8 * 2 ** 20 * 2 * 3)


if __name__ == '__main__':
    # mh = MultipleHash(["1", "2", "3"])
    # print(mh.get_hash_values("asdasfasd"))
    data = ["asdfasdf", "123", "123", "456", "asf", "asf"]
    salts = ["1", "2", "3", "4"]
    bm = BloomFilter(salts=salts)
    for d in data:
        if not bm.is_exists(d):
            bm.save(d)
            print("{0} save success".format(d))
        else:
            print("find repeat data {0}".format(d))
