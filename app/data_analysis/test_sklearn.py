# -*- coding: utf-8 -*-

from sklearn import preprocessing
import numpy as np

# x = np.array([[0., -3., 1.],
#               [3., 1., 2.],
#               [0., 1., -1.]])
# x = np.array([[0., -3., 1.]])
x = np.array([[3., 1., 2.]])


def test_min_max():
    # 使用[0,1]规范化
    # 新数值 =（原数值 - 极小值）/（极大值 - 极小值）
    # 初始化数据，每一行表示一个样本，每一列表示一个特征
    min_max_scaler = preprocessing.MinMaxScaler()
    min_max_x = min_max_scaler.fit_transform(x)
    print(min_max_x)


if __name__ == '__main__':
    test_min_max()
