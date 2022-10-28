# 2-6 概率随着探测次数的变化
import argparse
import equations
import matplotlib.pyplot as plt
from env import create_env
from scipy.interpolate import make_interp_spline
from smooth_line import plot_smooth_lines
import numpy as np
from equations import *


def main():
    "************************"
    x = [i for i in range(0, 10, 1)]  # 探测次数
    y1 = [0.5]
    tmp_y = 0.5
    for i in range(len(x) - 1):
        tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 0)
        y1.append(tmp_y)
    plt.plot(x, y1, label="不存在目标，且全探测正确", linestyle="-", marker="*")

    "************************"
    x = [i for i in range(0, 10, 1)]  # 探测次数
    y1 = [0.5]
    tmp_y = 0.5
    for i in range(len(x) - 1):
        tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 1)
        y1.append(tmp_y)
    plt.plot(x, y1, label="存在目标，且全探测正确", linestyle="-", marker="^")

    "************************"
    x = [i for i in range(0, 10, 1)]  # 探测次数
    y1 = [0.5]
    tmp_y = 0.5
    for i in range(len(x) - 1):
        if i == 0:
            tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 0)
        else:
            tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 1)
        y1.append(tmp_y)
    plt.plot(x, y1, label="存在目标，且仅第一次探测错误", linestyle="-.", marker="d")

    "************************"
    x = [i for i in range(0, 10, 1)]  # 探测次数
    y1 = [0.5]
    tmp_y = 0.5
    for i in range(len(x) - 1):
        if i == 1:
            tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 0)
        else:
            tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 1)
        y1.append(tmp_y)
    plt.plot(x, y1, label="存在目标，且仅第二次探测错误", linestyle=":", marker="*")

    "************************"
    x = [i for i in range(0, 10, 1)]  # 探测次数
    y1 = [0.5]
    tmp_y = 0.5
    for i in range(len(x) - 1):
        if i == 2:
            tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 0)
        else:
            tmp_y = update_exist_prob(tmp_y, 0.9, 0.1, 1)
        y1.append(tmp_y)
    plt.plot(x, y1, label="存在目标，且仅第三次探测错误", linestyle="-.", marker="o")

    # 设置横纵坐标的名称以及对应字体格式
    size=12

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # https: // blog.csdn.net / Wannna / article / details / 102751689
    plt.xlabel('探测次数', fontsize=size)
    plt.ylabel('目标存在概率', fontsize=size)
    # 设置刻度字体大小
    plt.xticks(fontsize=size)
    plt.yticks(fontsize=size)

    plt.legend(loc=7, fontsize=size)
    plt.savefig("概率随探测次数的变化.jpg", dpi=120)
    plt.show()


# 定义参数
if __name__ == '__main__':
    main()
