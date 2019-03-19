# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# # projection='3d'的意思是绘制三维图形，否则绘制的就是平面图形，彩蛋就不会那么立体了
# ax = fig.gca(projection='3d')
#
# x = 10 * np.outer(np.cos(u), np.sin(v))
# y = 10 * np.outer(np.sin(u), np.sin(v))
# z = 6 * np.outer(np.ones(np.size(u)), np.cos(v))
# ax.plot_surface(x, y, z, cmap=plt.cm.get_cmap(value))

# # x, y, z 均为 0 到 1 之间的 100 个随机数
# x = np.random.normal(0, 1, 100)
# y = np.random.normal(0, 1, 100)
# z = np.random.normal(0, 1, 100)


def line_pic():
    # 生成数据
    x = np.linspace(-6 * np.pi, 6 * np.pi, 1000)
    y = np.sign(x)
    z = np.cos(x)

    # 创建图形对象
    fig = plt.figure()
    ax = Axes3D(fig)
    # 绘制散点图
    # ax.scatter(x, y, z)

    # 绘制线形图
    ax.plot(x, y, z)
    plt.show()


def circle_pic():
    fig = plt.figure()
    ax = Axes3D(fig)

    # 生成数据
    x = np.arange(-2, 2, 0.1)
    y = np.arange(-2, 2, 0.1)
    x, y = np.meshgrid(x, y)
    z = np.sqrt(x ** 2 + y ** 2)

    # 绘制曲面图, 用cmap着色
    ax.plot_surface(x, y, z, cmap=plt.cm.winter)
    plt.show()
    plt.clf()
    plt.close()


def mix_pic():
    fig = plt.figure()
    ax = Axes3D(fig)

    x = np.linspace(-3 * np.pi, 3 * np.pi, 500)
    y = np.sign(x)
    ax.plot(x, y, zs=0, c='red')

    xx = np.random.normal(0, 1, 100)
    yy = np.random.normal(0, 1, 100)
    zz = np.random.normal(0, 1, 100)
    ax.scatter(xx, yy, zz)

    plt.show()


def child_pic():
    fig = plt.figure()

    # 向画布添加子图 1
    add_ax = fig.add_subplot(1, 2, 1, projection='3d')

    x = np.linspace(-6 * np.pi, 6 * np.pi, 2000)
    y = np.sin(x)
    z = np.cos(x)
    add_ax.plot(x, y, z)

    # 向画布添加子图 2
    add_ax_2 = fig.add_subplot(1, 2, 2, projection='3d')
    # 生成子图2
    x = np.arange(-2, 2, 0.1)
    y = np.arange(-2, 2, 0.1)
    x, y = np.meshgrid(x, y)
    z = np.sqrt(x ** 2 + y ** 2)
    add_ax_2.plot_surface(x, y, z, cmap=plt.cm.winter)

    plt.show()


if __name__ == '__main__':
    # circle_pic()
    # mix_pic()
    child_pic()
