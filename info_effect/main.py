# 主要是用于测试无人机信息共享的效果
import argparse
import equations
import seaborn as sns
import matplotlib.pyplot as plt
from env import create_env
from scipy.interpolate import make_interp_spline
from smooth_line import plot_smooth_lines
import numpy as np


def render(prob_map, com_times, search_step):
    plt.figure()
    plt.clf()
    # 调色盘 https://www.cnblogs.com/Forever77/p/11396588.html
    # sns.heatmap https://zhuanlan.zhihu.com/p/165426873
    sns.heatmap(prob_map, vmin=0.5, vmax=1, linewidths=1, annot=True,
                cmap=sns.color_palette('YlGnBu', 30), fmt=".2f",
                annot_kws={'color': 'black'}).invert_yaxis()
    plt.savefig(str(search_step) + "_" + str(com_times-1) + "次错误探测后的纠正效果.jpg", dpi=240)
    plt.pause(10)


def main(args):
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
            if (com_times == 4) and (search_step == 1 or search_step == 2 or search_step == 3):
                render(env.agents_unc[args.layers][args.layers], com_times, search_step)
            if com_times == 8:
                render(env.agents_unc[args.layers][args.layers], com_times, search_step)
            env.agent_com()
            # 记录中间无人机所记录的中间数值
            uncertainties.append(env.agents_unc[args.layers][args.layers][args.layers][args.layers])
        uncertainties_all.append(uncertainties)

    linestyles = ["-", ":", "-.", "_"]

    # 绘制目标存在概率随着交互次数的影响，图一
    for i in range(args.max_step):
        # 对x和y1进行插值
        x = np.linspace(0, args.max_com_time, len(uncertainties_all[i]))
        x_smooth = np.linspace(0, args.max_com_time, len(uncertainties_all[i]) * 10)
        y1_smooth = make_interp_spline(x, uncertainties_all[i])(x_smooth)
        # plt.plot(uncertainties_all[i])
        perLable = "Detect " + str(i + 1) + " times before communication"
        plt.plot(x_smooth, y1_smooth, label=perLable, linestyle=linestyles[i])
        plt.axis([0, args.max_com_time, 0.725, 1.1])
    # https: // blog.csdn.net / Wannna / article / details / 102751689
    plt.xlabel('Communication times')
    plt.ylabel('Existing probability')
    plt.legend(loc=1)
    plt.show()


# 定义参数
if __name__ == '__main__':
    # 环境相关基本要素
    parser = argparse.ArgumentParser()
    parser.add_argument('--layers', default=5, type=int, help='无人机层数')
    parser.add_argument('--env_range', default=11, type=int, help='环境大小=2*layers+1')
    parser.add_argument('--detect_nums', default=1, type=int, help='单步检测次数')
    parser.add_argument('--max_step', default=3, type=int, help='最大步长')
    parser.add_argument('--max_com_time', default=10, type=int, help='单次搜索后信息交流次数')
    parser.add_argument('--alg2_n', default=3, type=int, help='算法2的幂指数,一定得是奇数')
    parser.add_argument('--prob_correct', default=0.9, type=int, help='无人机层数')
    parser.add_argument('--prob_false_alarm', default=0.1, type=int, help='无人机层数')
    parser.add_argument('--com_type', default='prop_alg2', type=str, help='prop_alg1/min_com/prob_equal')
    Args = parser.parse_args()
    main(Args)
