# -*- coding: utf-8 -*-

import redis

from . import BaseFilter


class RedisFilter(BaseFilter):
    """基于redis持久化存储的去重判断"""

    def _get_storage(self):
        """
        使用 Redis 连接池
        返回Redis连接对象
        :return: 返回Redis连接对象
        """
        # client = redis.StrictRedis(host='', port=6379, db=0)
        pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        client = redis.StrictRedis(connection_pool=pool)
        return client

    def _save(self, hash_value):
        """
        利用Redis无序集合进行存储
        :param hash_value:
        :return:
        """
        return self.storage.sadd(self.redis_key, hash_value)

    def _is_exists(self, hash_value):
        """判断Redis对应的无序集合中是否对应的判断依据"""
        return self.storage.sismember(self.redis_key, hash_value)


