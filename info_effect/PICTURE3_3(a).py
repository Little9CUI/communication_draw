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

    aim_prob = 0.1

    # 与base是0.9的情况进行融合分析，利用平均融合的情况
    y1 = []
    for i in range(len(x)):
        y_tmp = prob_equal(x[i], aim_prob) / 2
        y1.append(y_tmp)

    # 所提出的通信融合算法，并且n=3次幂
    y2 = []
    n = 3
    for i in range(len(x)):
        y_tmp = prop_alg2([[x[i]]], [[aim_prob]], n)
        y_tmp = math.pow(equations.exist_pro_to_log_pro(y_tmp[0][0]), n) / 2
        if y_tmp > 0:
            y_tmp = equations.log_pro_to_exist_pro(
                math.pow(y_tmp, 1 / n))
        else:
            y_tmp = equations.log_pro_to_exist_pro(
                -math.pow(-y_tmp, 1 / n))
        y2.append(y_tmp)

    # 所提出的通信融合算法，并且n=1次幂
    y3 = []
    n = 1
    for i in range(len(x)):
        y_tmp = prop_alg2([[x[i]]], [[aim_prob]], n)
        y_tmp = math.pow(equations.exist_pro_to_log_pro(y_tmp[0][0]), n) / 2
        if y_tmp > 0:
            y_tmp = equations.log_pro_to_exist_pro(
                math.pow(y_tmp, 1 / n))
        else:
            y_tmp = equations.log_pro_to_exist_pro(
                -math.pow(-y_tmp, 1 / n))
        y3.append(y_tmp)

    # 所提出的通信融合算法，并且n=5次幂
    y4 = []
    n = 5
    for i in range(len(x)):
        y_tmp = prop_alg2([[x[i]]], [[aim_prob]], n)
        y_tmp = math.pow(equations.exist_pro_to_log_pro(y_tmp[0][0]), n) / 2
        if y_tmp > 0:
            y_tmp = equations.log_pro_to_exist_pro(
                math.pow(y_tmp, 1 / n))
        else:
            y_tmp = equations.log_pro_to_exist_pro(
                -math.pow(-y_tmp, 1 / n))
        y4.append(y_tmp)

    # 取不确定度最小值的方法
    y5 = []
    for i in range(len(x)):
        y_tmp = min_com([[x[i]]], [[aim_prob]])
        y5.append(y_tmp[0][0])

    # 基于不确定度的加权取平均
    y6 = []
    for i in range(len(x)):
        y_tmp = prop_alg4(x[i], aim_prob)
        y6.append(y_tmp)

    # 绘图
    size = 14
    plt.plot(x, y1, label="基于概率取平均", linestyle=":")
    # plt.plot(x, y5, label="取不确定度最小值", linestyle="dotted")
    plt.plot(x, y6, label="基于不确定度的加权取平均", linestyle="-.")
    plt.plot(x, y3, label="基于信息量的n次方取平均(n=1)", linestyle="--")
    plt.plot(x, y2, label="基于信息量的n次方取平均(n=3)", linestyle='-')
    # plt.plot(x, y4, label="n=5", linestyle="-.")
    # plt.plot(x, val_baseline, linestyle=":")
    plt.xlabel("被融合的概率", fontsize=size)
    plt.ylabel("融合后的概率", fontsize=size)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 设置刻度字体大小
    plt.xticks(fontsize=size)
    plt.yticks(fontsize=size)
    plt.legend(loc=2, fontsize=size)
    plt.savefig("与不同概率值的融合效果(a).jpg", dpi=240)
    plt.show()


# 定义参数
if __name__ == '__main__':
    main()
