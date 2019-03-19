# -*- coding: utf-8 -*-

import requests
import json


class FanYi(object):
    def __init__(self):
        self.url = 'https://fanyi.baidu.com/basetrans'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"}

        self.query = input("请输入需要查询的中文:")

    def init_data(self):
        # 构造post请求字典
        data = {
            'query': self.query,
            'from': 'zh',
            'to': 'en',
            'token': 'b0c2bf1a6cf24cefcb89ebf29bf9248c',
            'sign': 973237.670340
        }
        return data

    # @staticmethod
    def get_data(self, data):
        res = requests.post(url=self.url, data=data, headers=self.headers)
        rep = json.loads(res.content.decode())
        print(rep)
        return rep['errno']

    def run(self):
        print(self.get_data(self.init_data()))
        # print(rep)


if __name__ == '__main__':

    fan_yi = FanYi()
    # result = fan_yi.init_data()
    # no = fan_yi.get_data(result)
    fan_yi.run()
