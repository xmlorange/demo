# -*- coding: utf-8 -*-

# [123, "123", "456", "qwe", "qwe"] ==> [123, "456", "qwe"]
ret = list()
sign = list()   # 原始数据的特征  判断依据
new_data = None

if str(new_data) not in sign:
    sign.append(str(new_data))
    ret.append(new_data)

# ret  : ["123", "456", "qwe"]
# sign : [123, "456", "qwe"]


# 去重容器  存储原始数据判断依据
