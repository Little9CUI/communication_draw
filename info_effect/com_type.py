import numpy as np
import equations
import math


def min_com(unc_1, unc_2):
    unc = np.ones([len(unc_1), len(unc_1[0])])
    for i in range(len(unc_1)):
        for j in range(len(unc_1[0])):
            if equations.exist_pro_to_det_value(unc_1[i][j]) < equations.exist_pro_to_det_value(unc_2[i][j]):
                unc[i][j] = unc_1[i][j]
            else:
                unc[i][j] = unc_2[i][j]
    return unc


def prob_equal(unc_1, unc_2):
    unc = unc_1 + unc_2
    return unc


# log形式的概率进行取平均，相当于后续的1次幂
def prop_alg1(unc_1, unc_2):
    unc = np.ones([len(unc_1), len(unc_1[0])])
    for i in range(len(unc_1)):
        for j in range(len(unc_1[0])):
            unc[i][j] = (equations.exist_pro_to_log_pro(unc_1[i][j]) + equations.exist_pro_to_log_pro(unc_2[i][j]))/2
            unc[i][j] = equations.log_pro_to_exist_pro(unc[i][j])
    return unc


# log形式的概率,先进性n次幂，再进行取平均，取平均的时候按照无人机个体数量进行平均
def prop_alg2(unc_1, unc_2, n):
    unc = np.ones([len(unc_1), len(unc_1[0])])
    for i in range(len(unc_1)):
        for j in range(len(unc_1[0])):
            unc[i][j] = math.pow(equations.exist_pro_to_log_pro(unc_1[i][j]), n) + math.pow(
                equations.exist_pro_to_log_pro(unc_2[i][j]), n)
            if unc[i][j] > 0:
                unc[i][j] = equations.log_pro_to_exist_pro(math.pow(unc[i][j], 1 / n))  # 负数不能开方
            else:
                unc[i][j] = equations.log_pro_to_exist_pro(-math.pow(-unc[i][j], 1 / n))  # 负数不能开方
    return unc


# log形式的概率,先进性n次幂，再进行取平均，取平均的时候按照n-3次幂的加和进行的平均
def prop_alg3(unc_total, unc_2, sum_index, n):
    for i in range(len(unc_total[0])):
        for j in range(len(unc_total[1])):
            log_prob = equations.exist_pro_to_log_pro(unc_2[i][j])
            unc_total[i][j] = unc_total[i][j] + math.pow(log_prob, n)
            sum_index[i][j] = sum_index[i][j] + math.pow(log_prob, n - 3)
    return unc_total, sum_index


# 以不确定度作为权重因子
def prop_alg4(prob1, prob2):
    unc_1 = equations.exist_pro_to_det_value(prob1)
    unc_2 = equations.exist_pro_to_det_value(prob2)
    res = ((1-unc_1) * prob1 + (1-unc_2) * prob2) / ((1-unc_1) + (1-unc_2)+0.0001)
    return res
