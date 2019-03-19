# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from pandas import DataFrame
from pandasql import sqldf, load_meat, load_births

PATH = "C:/Project/demo/demo.xlsx"


def to_excel():
    score = DataFrame(pd.read_excel(PATH))
    score.to_excel("demo_copy.xlsx")
    print(score)


def test_pandasql():
    df = DataFrame({'name': ['zhagfei', 'guanyu', 'a', 'b', 'c'], 'data1': range(5)})
    # pysqldf = lambda sql: sqldf(sql, locals())    python 2.7写法
    sql = "select * from df where name = 'zhagfei'"

    print(df)
    print('-' * 30)
    print(sqldf(sql, locals()))
    # print('-' * 30)
    # print(pysqldf(sql))


def reference_data():
    # 创建数据集并进行数据清洗：清除重复的行；
    # 录入数值时，空值用None或np.nan；defaultValues为字段为空时的默认值，姓名字段默认为“无姓名”，成绩字段默认为0
    # 分别使用drop_duplicates和fillna方法进行去重复值及空值填充
    data = {'Name': ['张飞', '关羽', '赵云', '黄忠', '典韦', '典韦'], 'Chinese': [66, 95, 95, 90, 80, 80],
            'English': [65, 85, 92, 88, 90, 90] , 'Maths': [None, 98, 96, 77, 90, 90]}
    df = DataFrame(data, columns=['Name', 'Chinese', 'English', 'Maths'])
    defaultValues = {'Name': '无姓名', 'Chinese': 0, 'English': 0, 'Maths': 0}
    df = df.drop_duplicates()
    # 按照默认值进行填充
    df = df.fillna(defaultValues)
    # 使用其他学生的平均值对空值进行填充
    # df['Maths'].fillna(df['Maths'].mean(), inplace=True)

    # 使用Pandas SQL进行排序语句编写
    pysqldf = lambda sql: sqldf(sql, globals())
    sql = "select *, Chinese + English + Maths as Total from df order by Chinese + English + Maths desc"
    print(pysqldf(sql))


if __name__ == '__main__':
    # to_excel()
    test_pandasql()
    # reference_data()
