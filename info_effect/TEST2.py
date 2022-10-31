# 主要是用于测试无人机信息共享的效果
import argparse
import equations
import matplotlib.pyplot as plt
from env import create_env
from scipy.interpolate import make_interp_spline
from smooth_line import plot_smooth_lines
import numpy as np
import math


def main():
    x = [i for i in range(0, 60, 1)]
    y = []
    y_test = []
    for element in x:
        tmp = 1 / (1 + math.exp(element/2-4))
        y.append(tmp)
        y_test.append(-(element/2-4) / 4 + 0.5)

    plt.plot(x, y)
    plt.plot(x, y_test)
    plt.axis([0, 20, 0, 1])
    plt.show()


# 定义参数
if __name__ == '__main__':
    main()
