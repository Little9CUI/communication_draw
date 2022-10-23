# 不同信息融合算法比较1，主要是基于0.9，如果想基于0.1，只需要把0.9改成0.1就行
# 主要是用于测试无人机信息共享的效果
import argparse
import equations
import matplotlib.pyplot as plt
import numpy as np
from com_type import *


def main():
    x = [x_val * 0.01 for x_val in range(0, 100, 1)]
    val_baseline = [0.5 for x_val in range(0, 100, 1)]

    # 与base是0.9的情况进行融合分析，利用平均融合的情况
    y1 = []
    for i in range(len(x)):
        y_tmp = prob_equal(x[i], 0.1) / 2
        y1.append(y_tmp)

    # 所提出的通信融合算法，并且n=3次幂
    y2 = []
    for i in range(len(x)):
        y_tmp = prop_alg2([[x[i]]], [[0.1]], 3)
        y2.append(y_tmp[0][0])

    # 所提出的通信融合算法，并且n=1次幂
    y3 = []
    for i in range(len(x)):
        y_tmp = prop_alg1([[x[i]]], [[0.1]])
        y3.append(y_tmp[0][0])

    # 所提出的通信融合算法，并且n=5次幂
    y4 = []
    for i in range(len(x)):
        y_tmp = prop_alg2([[x[i]]], [[0.1]], 5)
        y4.append(y_tmp[0][0])

    # 取不确定度最小值的方法
    y5 = []
    for i in range(len(x)):
        y_tmp = min_com([[x[i]]], [[0.1]])
        y5.append(y_tmp[0][0])

    # 所提出的通信融合算法，并且n=3次幂
    y6 = []
    for i in range(len(x)):
        y_tmp = prop_alg4(x[i], 0.1)
        y6.append(y_tmp)

    plt.plot(x, y1, label="基于概率取平均", linestyle=":")
    plt.plot(x, y6, label="基于不确定度的加权取平均", linestyle="-.")
    plt.plot(x, y2, label="基于信息量的n次方取平均(n=3)", linestyle='-')
    plt.plot(x, y3, label="基于信息量的n次方取平均(n=1)", linestyle="--")
    # plt.plot(x, y4, label="n=5", linestyle="-.")
    # plt.plot(x, y5, label="取不确定度最小值", linestyle="dotted")
    # plt.plot(x, val_baseline, linestyle=":")
    plt.xlabel("被融合的概率")
    plt.ylabel("融合后的概率")
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend(loc=2)
    plt.show()
    plt.pause(10)


# 定义参数
if __name__ == '__main__':
    main()
