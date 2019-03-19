# -*- coding: utf-8 -*-

# 基于信息摘要算法进行数据的去重判断和存储

# 1. 基于内存存储
# 2. 基于Redis的存储
# 3. 基于MySQL的存储

import hashlib

import six


class BaseFilter(object):
    """基于信息摘要算法进行数据的去重判断和存储"""

    def __init__(self,
                 hash_func_name='md5',
                 redis_host='localhost',
                 redis_port=6379,
                 redis_db=0,
                 redis_key='filter',
                 mysql_url=None,
                 mysql_table_name='filter'):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_key = redis_key

        self.mysql_url = mysql_url
        self.mysql_table_name = mysql_table_name

        self.hash_func = getattr(hashlib, hash_func_name)
        self.storage = self._get_storage()

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

    def _get_hash_value(self, data):
        """
        根据给定数据，返回的对应摘要的hash值
        :param data: 给定的原始数据(二进制类型的字符串数据)
        :return: hash 值
        """
        hash_obj = self.hash_func()
        hash_obj.update(self._safe_data(data))  # python3 data must bytes  python2 str
        hash_value = hash_obj.hexdigest()
        return hash_value

    def save(self, data):
        """
        根据 data 计算出对应的指纹进行存储
        :param data: 给定的原始数据(二进制类型的字符串数据)
        :return: 返回存储的结果
        """
        hash_value = self._get_hash_value(data)
        return self._save(hash_value)

    def _save(self, hash_value):
        """
        存储对应的hash值
        交给对应的子类继承去重写
        :param hash_value: 通过信息摘要算法求出hash值
        :return: 存储结果
        """
        pass

    def is_exists(self, data):
        """
        判断给定的数据是否存在
        :param data: 给定的原始数据(二进制类型的字符串数据)
        :return: True or False
        """
        hash_value = self._get_hash_value(data)
        return self._is_exists(hash_value)

    def _is_exists(self, hash_value):
        """
        判断对应的hash值已经存在 (交给对应子类继承)
        :param hash_value: 通过信息摘要算法求出hash值
        :return: True or False
        """
        pass

    def _get_storage(self):
        """
        返回对应的存储对象 (交给子类去继承)
        :return:
        """
        pass


if __name__ == '__main__':
    base = BaseFilter()
