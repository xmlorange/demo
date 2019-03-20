# -*- coding: utf-8 -*-
from pymongo import MongoClient


def test_mongo():
    client = MongoClient(host='localhost', port=27017)
    db = client.test_db
    collection = db.test_cllection

    data = {
        "title": "python 数据分析",
        "author": "John Goerzen",
        "publisher": "人民邮电出版社",
        "info": {
            "producer": "新经典文化",
            "translator": "韩波",
            "price": 43.5,
            "pack": "精装"
        },
        "isbn": "98756424244",
        "rating_num": 8.6,
        "another_data": [1, 23, "new data"]
    }
    # 插入数据
    # obj = db.book.insert_one(data)
    # print(obj.inserted_id)

    # 查询数据
    ret = db.book.find_one({"author": "John Goerzen"})
    print(ret)

    # 更新数据
    # ret = db.book.update({"title": "python 数据分析"}, {"$set": {"title": "《python 数据分析》"}})
    # print(ret)


if __name__ == '__main__':
    test_mongo()
