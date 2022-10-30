# 概率值随着探测次数的变化

import argparse
import equations
import matplotlib.pyplot as plt
import numpy as np
from com_type import *
from equations import *


def main():
    x = [i * 0.001 for i in range(1, 1000, 1)]

    prob_change = []
    for i in range(len(x)):
        prob = exist_pro_to_log_pro(x[i])
        prob_change.append(prob)

    tmp = []
    for i in range(len(x)):
        tmp.append(0)

    # 设置横纵坐标的名称以及对应字体格式
    size = 15
    plt.plot(x, prob_change, label="信息量随概率的变化曲线", linestyle="-")
    plt.plot(x, tmp, linestyle=":")
    plt.xlabel('目标存在概率', fontsize=size)
    plt.ylabel('信息量', fontsize=size)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.legend(loc=7, fontsize=size, bbox_to_anchor=(0.95, 0.8))
    # 设置刻度字体大小
    plt.xticks(fontsize=size)
    plt.yticks(fontsize=size)
    # plt.axis([-0.1, 1.1, -22, 22])
    plt.savefig("信息量随概率的变化曲线.jpg", dpi=240)
    plt.show()


# 定义参数
if __name__ == '__main__':
    main()
