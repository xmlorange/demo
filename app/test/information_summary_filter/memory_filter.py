# -*- coding: utf-8 -*-

from . import BaseFilter


class MemoryFilter(BaseFilter):
    """基于python中的 集合数据结构进行去重判断依据的存储"""

    def _get_storage(self):
        return set()

    def _save(self, hash_value):
        """
        利用 set 进行存储
        :param hash_value:
        :return:
        """
        return self.storage.add(hash_value)

    def _is_exists(self, hash_value):
        if hash_value in self.storage:
            return True
        return False
