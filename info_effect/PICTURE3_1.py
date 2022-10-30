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

    # 设置横纵坐标的名称以及对应字体格式
    size = 15
    plt.plot(x, prob_change, label="概率值随探测次数的变化", linestyle="-")
    plt.plot(x, inform_change, label="信息量随探测次数的变化", linestyle="-.")
    # plt.plot(x, unc_change, label="不确定度随探测次数的变化", linestyle="--")
    plt.xlabel('无人机探测次数', fontsize=size)
    plt.ylabel('不同类型数据的数值', fontsize=size)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend(loc=7, fontsize=size, bbox_to_anchor=(0.95, 0.6))
    # 设置刻度字体大小
    plt.xticks(fontsize=size)
    plt.yticks(fontsize=size)
    plt.axis([-0.5, 10, -12, 2])
    plt.savefig("不同值随探测次数的变化.jpg", dpi=240)
    plt.show()


# 定义参数
if __name__ == '__main__':
    main()
