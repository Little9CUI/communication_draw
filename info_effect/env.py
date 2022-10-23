import numpy as np
import com_type
import equations
import math


def create_env(args):
    env = RawEnv(args)
    return env


class RawEnv:
    def __init__(self, args):
        self.env_range = args.env_range
        self.com_type = args.com_type
        self.layers = args.layers
        self.alg_2_n = args.alg2_n
        self.agents_unc = 0.5 * np.ones([args.env_range, args.env_range, args.env_range, args.env_range])
        self.agents_unc_pre = np.ones([args.env_range, args.env_range, args.env_range, args.env_range])

    # 无人机之间的单次信息交互
    def agent_com(self):
        self.agents_unc_pre = self.agents_unc.copy()
        for i in range(self.env_range):
            for j in range(self.env_range):
                if self.com_type == 'min_com':  # 根据不同的交互类型进行选择
                    self.min_com(i, j)
                elif self.com_type == 'prop_alg1':
                    self.prop_alg1(i, j)
                elif self.com_type == 'prob_equal':
                    self.prob_equal(i, j)
                elif self.com_type == 'prop_alg2':
                    self.prop_alg2(i, j)
                elif self.com_type == 'prop_alg3':
                    self.prop_alg3(i, j)

    # 下面是一些通信的交互的函数实现
    def min_com(self, i, j):
        com_list = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        for k in range(len(com_list)):
            if (0 <= i + com_list[k][0] < self.env_range) & (0 <= j + com_list[k][1] < self.env_range):
                self.agents_unc[i][j] = com_type.min_com(
                    self.agents_unc_pre[i + com_list[k][0]][j + com_list[k][1]],
                    self.agents_unc[i][j])

    def prop_alg1(self, i, j):
        com_list = [[1, 0], [0, -1], [0, 1], [-1, 0]]
        count = 1  # 用于prop_alg1模式中取平均
        for k in range(len(com_list)):
            if (0 <= i + com_list[k][0] < self.env_range) & (0 <= j + com_list[k][1] < self.env_range):
                count = count + 1
                self.agents_unc[i][j] = com_type.prop_alg1(
                    self.agents_unc_pre[i + com_list[k][0]][j + com_list[k][1]],
                    self.agents_unc[i][j])
        for k in range(self.env_range):
            for g in range(self.env_range):
                self.agents_unc[i][j][k][g] = equations.exist_pro_to_log_pro(self.agents_unc[i][j][k][g]) / count
                self.agents_unc[i][j][k][g] = equations.log_pro_to_exist_pro(self.agents_unc[i][j][k][g])

    def prob_equal(self, i, j):
        com_list = [[1, 0], [0, -1], [0, 1], [-1, 0]]
        count = 1  # 用于prop_alg1模式中取平均
        for k in range(len(com_list)):
            if (0 <= i + com_list[k][0] < self.env_range) & (0 <= j + com_list[k][1] < self.env_range):
                count = count + 1
                self.agents_unc[i][j] = com_type.prob_equal(
                    self.agents_unc_pre[i + com_list[k][0]][j + com_list[k][1]],
                    self.agents_unc[i][j])
        self.agents_unc[i][j] = self.agents_unc[i][j] / count

    def prop_alg2(self, i, j):
        com_list = [[1, 0], [0, -1], [0, 1], [-1, 0]]
        count = 1  # 用于prop_alg1模式中取平均
        for k in range(len(com_list)):
            if (0 <= i + com_list[k][0] < self.env_range) & (0 <= j + com_list[k][1] < self.env_range):
                count = count + 1
                self.agents_unc[i][j] = com_type.prop_alg2(
                    self.agents_unc_pre[i + com_list[k][0]][j + com_list[k][1]],
                    self.agents_unc[i][j], self.alg_2_n)
        for k in range(self.env_range):
            for g in range(self.env_range):
                self.agents_unc[i][j][k][g] = math.pow(equations.exist_pro_to_log_pro(self.agents_unc[i][j][k][g]),
                                                       self.alg_2_n) / count
                if self.agents_unc[i][j][k][g] > 0:
                    self.agents_unc[i][j][k][g] = equations.log_pro_to_exist_pro(
                        math.pow(self.agents_unc[i][j][k][g], 1 / self.alg_2_n))
                else:
                    self.agents_unc[i][j][k][g] = equations.log_pro_to_exist_pro(
                        -math.pow(-self.agents_unc[i][j][k][g], 1 / self.alg_2_n))

    # 将log模式作为加权的系数，而不进行开方
    def prop_alg3(self, i, j):
        com_list = [[1, 0], [0, -1], [0, 1], [-1, 0], [0, 0]]
        count = 1  # 用于prop_alg1模式中取平均
        n = 3  # n次幂
        unc_total = np.zeros((self.env_range, self.env_range), dtype=float)
        sum_index = np.zeros((self.env_range, self.env_range), dtype=float)
        for k in range(len(com_list)):
            if (0 <= i + com_list[k][0] < self.env_range) & (0 <= j + com_list[k][1] < self.env_range):
                count = count + 1
                unc_total, sum_index = com_type.prop_alg3(unc_total,
                                                          self.agents_unc_pre[i + com_list[k][0]][j + com_list[k][1]],
                                                          sum_index, self.alg_2_n)
        for k in range(self.env_range):
            for g in range(self.env_range):
                log_prob = equations.exist_pro_to_log_pro(self.agents_unc_pre[i][j][k][g])
                if sum_index[k][g] == 0:
                    unc_total[k][g] = 0
                else:
                    unc_total[k][g] = unc_total[k][g] / sum_index[k][g]# * math.pow(log_prob, n - 1)
                self.agents_unc[i][j][k][g] = equations.log_pro_to_exist_pro(unc_total[k][g])
