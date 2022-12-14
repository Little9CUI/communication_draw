import math


# 更新目标存在概率的公式
def update_exist_prob(exist_prob, prob_correct, prob_false_alarm, whether_exist):
    if whether_exist == 1:
        exist_prob = exist_prob * prob_correct / (exist_prob * prob_correct + prob_false_alarm * (1 - exist_prob))
    else:
        exist_prob = exist_prob * (1 - prob_correct) / (
                exist_prob * (1 - prob_correct) + (1 - prob_false_alarm) * (1 - exist_prob))  # 没整明白是为什么？？？？？？？？
    return exist_prob


# 目标存在概率到探测价值的转换
def exist_pro_to_det_value(exist_prob):
    k = 2
    det_value = exist_pro_to_log_pro(exist_prob)
    det_value = math.exp(-k * abs(det_value))
    return det_value


# 目标存在概率的log形式转换
def exist_pro_to_log_pro(exist_prob):
    if exist_prob <= 0.00001:
        exist_prob = 1e-6
    elif exist_prob >= 0.99999:
        exist_prob = 0.99999
    log_pro = math.log(1 / exist_prob - 1)
    return log_pro


# 目标存在概率的log形式反转换
def log_pro_to_exist_pro(log_pro):
    exist_pro = 1/(math.exp(log_pro)+1)
    return exist_pro


def sigmoid(x):
    if x >= 0:
        z = math.exp(-x)
        sig = 1 / (1 + z)
        return sig
    else:
        z = math.exp(x)
        sig = z / (1 + z)
        return sig
