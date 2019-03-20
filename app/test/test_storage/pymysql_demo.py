# -*- coding: utf-8 -*-

import pymysql.cursors


class PyMysqlUsage(object):
    def __init__(self,
                 host='118.31.115.234',
                 port=3306,
                 user='root',
                 password='Bytech123',
                 db='business_uat_2',
                 charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor):
        # 连接数据库
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            charset=charset,
            cursorclass=cursorclass)
        print("数据库连接已建立")

    def create_table(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            self.connection.commit()

    def drop_table(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            self.connection.commit()

    def insert(self, sql, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            self.connection.commit()

    def select_all(self, sql, params=None):
        results = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
        return results

    def select_many(self, sql, params=None, size=1):
        results = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchmany(size)
        return results

    def select_one(self, sql, params=None):
        result = None
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()
        return result

    def __del__(self):
        self.connection.close()
        print("已断开数据库连接")


if __name__ == '__main__':
    obj = PyMysqlUsage()
    create_sql = """
        create table test_table(
            id int(11) NOT NULL AUTO_INCREMENT,
            name varchar(255) NOT NULL,
            age int(11) NOT NULL,
             PRIMARY KEY (`id`)
        ) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1;"""
    # obj.create_table(create_sql)

    drop_sql = """drop table test_table"""

    insert_sql = """Insert into test_table (name, age) values(%s, %s)"""
    # obj.insert(insert_sql, ("xuml", 25))

    query_all = "select * from test_table;"
    ret = obj.select_all(query_all)
    print("all: {}".format(ret))
