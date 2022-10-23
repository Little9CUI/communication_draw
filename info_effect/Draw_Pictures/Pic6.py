# 概率值随着探测次数的变化

import argparse
import equations
import matplotlib.pyplot as plt
import numpy as np
from com_type import *
from equations import *


def main():
    x = [i for i in range(0, 10, 1)]

    prob_change = [0.5]
    inform_change = [0]
    unc_change = [1]
    prob = 0.5
    for i in range(len(x) - 1):
        prob = update_exist_prob(prob, 0.9, 0.1, 1)
        inform = equations.exist_pro_to_log_pro(prob)
        unc = equations.exist_pro_to_det_value(prob)
        prob_change.append(prob)
        inform_change.append(inform)
        unc_change.append(unc)

    plt.plot(x, prob_change, label="概率随探测次数的变化", linestyle="-")
    plt.plot(x, inform_change, label="信息量随探测次数的变化", linestyle="-.")
    plt.plot(x, unc_change, label="不确定度随探测次数的变化", linestyle="--")
    plt.xlabel('无人机探测次数')
    plt.ylabel('不同类型信息的数值')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend(loc=3)
    plt.show()
    plt.pause(10)


# 定义参数
if __name__ == '__main__':
    main()
