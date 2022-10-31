# 主要是用于测试无人机信息共享的效果
import argparse
import equations
import matplotlib.pyplot as plt
from env import create_env
from scipy.interpolate import make_interp_spline
from smooth_line import plot_smooth_lines
import numpy as np
import math


def main(args):
    for alg2_n in range(1, 9, 2):
        args.alg2_n = alg2_n
        env = create_env(args)
        search_step = 0
        uncertainties = []
        uncertainties_all = []
        # 搜索的次数，一次搜索指的是无人机进行N次探测，然后进行M次的交互
        while search_step < args.max_step:
            search_step = search_step + 1
            args.detect_nums = search_step
            # 更新每次搜索的概率，假定每次发现有目标
            detect_num = 0
            env.agents_unc = 0.5 * np.ones([args.env_range, args.env_range, args.env_range, args.env_range])
            while detect_num < args.detect_nums:
                detect_num = detect_num + 1
                for i in range(args.env_range):
                    for j in range(args.env_range):
                        env.agents_unc[i][j][i][j] = equations.update_exist_prob(env.agents_unc[i][j][i][j],
                                                                                 args.prob_correct,
                                                                                 args.prob_false_alarm, 1)
            # 进行n次信息交互
            com_times = 0
            # 用于记录中间无人机所记录的中间数值
            uncertainties = [env.agents_unc[args.layers][args.layers][args.layers][args.layers]]
            while com_times < args.max_com_time:
                com_times = com_times + 1
                env.agent_com()
                # 记录中间无人机所记录的中间数值
                tmp = 1 / (1 + math.exp(com_times / 2 - 3))
                w = 1 / max((com_times - 1), 1)
                w=tmp
                env.agents_unc[args.layers][args.layers][args.layers][args.layers] = \
                    (1 - w) * env.agents_unc[args.layers][args.layers][args.layers][args.layers] + w * \
                    env.agents_unc_pre[args.layers][args.layers][args.layers][args.layers]

                uncertainties.append(env.agents_unc[args.layers][args.layers][args.layers][args.layers])
            uncertainties_all.append(uncertainties)

        linestyles = ["-", ":", "-.", "_"]

        # 绘制目标存在概率随着交互次数的影响，图一
        for i in range(args.max_step):
            # 对x和y1进行插值
            x = np.linspace(0, args.max_com_time, len(uncertainties_all[i]))
            # x_smooth = np.linspace(0, args.max_com_time, len(uncertainties_all[i]) * 10)
            # y1_smooth = make_interp_spline(x, uncertainties_all[i])(x_smooth)
            # plt.plot(uncertainties_all[i])
            perLable = "通信前进行 " + str(i + 1) + " 次探测"
            plt.plot(x, uncertainties_all[i], label=perLable, linestyle=linestyles[i])
            # plt.axis([0, args.max_com_time, 0.725, 1.1])
        # https: // blog.csdn.net / Wannna / article / details / 102751689

        # 绘图
        size = 14
        plt.xlabel('通信交互次数', fontsize=size)
        plt.ylabel('目标存在概率', fontsize=size)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 设置刻度字体大小
        plt.xticks(fontsize=size)
        plt.yticks(fontsize=size)
        plt.legend(loc=1, fontsize=size)#bbox_to_anchor=(0.95, 0.45))
        plt.savefig("修正版"+"概率值随通信次数的变化（n=" + str(args.alg2_n) + ").jpg", dpi=240)
        plt.show()


# 定义参数
if __name__ == '__main__':
    # 环境相关基本要素
    parser = argparse.ArgumentParser()
    parser.add_argument('--layers', default=5, type=int, help='无人机层数')
    parser.add_argument('--env_range', default=11, type=int, help='环境大小=2*layers+1')
    parser.add_argument('--detect_nums', default=1, type=int, help='单步检测次数')
    parser.add_argument('--max_step', default=3, type=int, help='最大步长')
    parser.add_argument('--max_com_time', default=50, type=int, help='单次搜索后信息交流次数')
    parser.add_argument('--alg2_n', default=7, type=int, help='算法2的幂指数,一定得是奇数')
    parser.add_argument('--prob_correct', default=0.9, type=int, help='无人机层数')
    parser.add_argument('--prob_false_alarm', default=0.1, type=int, help='无人机层数')
    parser.add_argument('--com_type', default='prop_alg2', type=str, help='prop_alg1/min_com/prob_equal')
    Args = parser.parse_args()
    main(Args)
