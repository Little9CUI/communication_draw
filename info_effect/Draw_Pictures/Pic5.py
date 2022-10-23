# 效果不好，暂时不用
# 主要是用于测试无人机信息共享的效果
import argparse
import equations
import matplotlib.pyplot as plt
import numpy as np
from com_type import *
from equations import *


def main():
    prob = 0.9
    prob_1 = update_exist_prob(prob, 0.9, 0.1, 1)  # 两次探索
    prob_2 = update_exist_prob(prob_1, 0.9, 0.1, 1)  # 三次探索

    x = [i for i in range(1, 7, 1)]

    # 单次搜索结果,利用prob_equal
    res1 = []
    for i in range(len(x)):
        tmp_prob = prob
        for j in range(x[i]):
            tmp_prob = prob_equal(tmp_prob, 0.5)
        tmp_res = tmp_prob / (x[i]+1)
        res1.append(tmp_res)

    # 单次搜索结果,利用prob_equal
    res2 = []
    for i in range(len(x)):
        tmp_prob = prob * (1-exist_pro_to_det_value(prob))
        tmp_fenMu = (1-exist_pro_to_det_value(prob))
        for j in range(x[i]):
            tmp_prob = tmp_prob + 0.5 * (1-exist_pro_to_det_value(0.5))
            tmp_fenMu = tmp_fenMu + (1-exist_pro_to_det_value(0.5))
        tmp_res = tmp_prob / tmp_fenMu
        res2.append(tmp_res)

    # 单次搜索结果,利用prop_alg2
    res3 = []
    for i in range(len(x)):
        tmp_prob = prob
        for j in range(x[i]):
            tmp_prob = prop_alg2([[prob]], [[0.5]], 3)
        tmp_res = tmp_prob/x[i]
        res3.append(tmp_res[0][0])

    # 单次搜索结果,利用prop_alg2
    res4 = []
    for i in range(len(x)):
        tmp_prob = prob
        for j in range(x[i]):
            tmp_prob = prop_alg2([[prob]], [[0.5]], 1)
        tmp_res = tmp_prob/x[i]
        res4.append(tmp_res[0][0])

    plt.plot(x, res1, label="基于概率取平均", linestyle=":")
    plt.plot(x, res2, label="基于不确定度的加权取平均", linestyle="-.")
    plt.plot(x, res3, label="基于信息量的n次方取平均(n=3)", linestyle='-')
    plt.plot(x, res4, label="基于信息量的n次方取平均(n=1)", linestyle="--")
    plt.xlabel('来自其他无人机的信息量')
    plt.ylabel('融合后的概率值')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend(loc=1)
    plt.show()
    plt.pause(10)


# 定义参数
if __name__ == '__main__':
    main()
