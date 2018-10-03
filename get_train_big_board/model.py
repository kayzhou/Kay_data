# -*- coding: utf-8 -*-
__author__ = 'Kay'

import numpy as np
from sklearn import datasets

def one_liner_model(p0, p1):
    '''
    :param p0: 常数项
    :param p1: 系数
    :return: 一元线性模型
    '''
    def model(x):
        return p0 + p1 * x
    return model

def two_liner_model(p0, p1, p2):
    '''
    :param p0: 常数项
    :param p1: 系数-1
    :param p2: 系数-2
    :return: 二元线性模型
    '''
    def model(x1, x2):
        return p0 + p1 * x1 + p2 * x2
    return model

def thr_liner_model(p0, p1, p2, p3):
    '''
    :param p0: 常数项
    :param p1: 系数-1
    :param p2: 系数-2
    :return: 三元线性模型
    '''
    def model(x1, x2, x3):
        return p0 + p1 * x1 + p2 * x2 + p3 * x3
    return model

def get_precision(li1, li2):
    '''
    :param li1: 真实数据
    :param li2: 预测数据
    :return:
    '''
    bingo = 0.0
    TP = FP = FN = TN = 0.0
    if len(li1) != len(li2):
        print('出错：列表大小不同')
        return False

    for i in range(len(li1)):
        if li1[i] == li2[i]:
            bingo += 1
            if li1[i] > 0:
                TP += 1
            else:
                TN += 1
        else:
            if li1[i] > 0:
                FN += 1
            else:
                FP += 1
    print '准确率:', bingo / len(li1), ' 命中数:', bingo, ' 总数:', len(li1)

    # 二分类问题更复杂的解释
    print 'TP:', TP / (TP + FN), 'TN:', TN / (FP + TN)
    print 'FP:', FP / (FP + TN), 'FN:', FN / (TP + FN)
    print '正样本:', TP + FN, '负样本:', FP + TN
    print '预测为正:', TP + FP, '预测为负:', TN + FN, '\n'

def get_class(li):
    re = list()
    for l in li:
        re.append(1 if l >= 0 else 0)
    return re

def use_bili():

    txt_data = np.loadtxt('data/just_bili.txt', float)
    close = txt_data[:, 0]
    high = txt_data[:, 1]
    low = txt_data[:, 2]
    hate_1 = txt_data[:, 4]
    happy_1 = txt_data[:, 5]
    sad_2 = txt_data[:, 11]
    hate_3 = txt_data[:, 14]
    sad_4 = txt_data[:, 21]

    t_txt_data = np.loadtxt('data/test_bili.txt', float)
    t_close = t_txt_data[:, 0]
    t_high = t_txt_data[:, 1]
    t_low = t_txt_data[:, 2]
    t_hate_1 = t_txt_data[:, 4]
    t_happy_1 = t_txt_data[:, 5]
    t_sad_2 = t_txt_data[:, 11]
    t_hate_3 = t_txt_data[:, 14]
    t_sad_4 = t_txt_data[:, 21]

    '''
    GOAL: CLOSE
    '''
    # model_1 = one_liner_model(1.63 ,-24.33)
    # y = list()
    # for x in sad_4:
    #     y.append(model_1(x))
    # t_y = list()
    # for i in range(len(t_txt_data)):
    #     t_y.append(model_1(t_sad_4[i]))
    #
    # # for i in range(len(y)):
    # #     print(close[i], y[i])
    # get_precision(get_class(close), get_class(y))
    # get_precision(get_class(t_close), get_class(t_y))
    #
    # # 只有比例，及比例和总量，做逐步回归
    # y = list()
    # model_2 = two_liner_model(0.9648, 31.18, -45.16)
    # for i in range(len(txt_data)):
    #     y.append(model_2(sad_2[i], sad_4[i]))
    # t_y = list()
    # for i in range(len(t_txt_data)):
    #     t_y.append(model_2(t_sad_2[i], t_sad_4[i]))
    #
    # # for i in range(len(t_y)):
    # #     print(t_close[i], t_y[i])
    # get_precision(get_class(close), get_class(y))
    # get_precision(get_class(t_close), get_class(t_y))

    '''
    GOAL: HIGH
    '''
    model_1 = one_liner_model(0.304, 16.408)
    y = list()
    for x in sad_2:
        y.append(model_1(x))
    t_y = list()
    for i in range(len(t_txt_data)):
        t_y.append(model_1(t_sad_2[i]))
    # for i in range(len(y)):
    #     print(close[i], y[i])
    # get_precision(get_class(high), get_class(y))
    # get_precision(get_class(t_high), get_class(t_y))

    y = list()
    model_2 = two_liner_model(-2.140, 22.675, 12.399)
    for i in range(len(txt_data)):
        y.append(model_2(sad_2[i], hate_3[i]))
    t_y = list()
    for i in range(len(t_txt_data)):
        t_y.append(model_2(t_sad_2[i], t_hate_3[i]))
    # for i in range(len(t_y)):
    #     print(high[i], t_y[i])
    # get_precision(get_class(high), get_class(y))
    # get_precision(get_class(t_high), get_class(t_y))

    y = list()
    model_3 = thr_liner_model(-0.202, 15.230, 19.308, -15.928)
    for i in range(len(txt_data)):
        y.append(model_3(sad_2[i], hate_3[i], hate_1[i]))
    t_y = list()
    for i in range(len(t_txt_data)):
        t_y.append(model_3(t_sad_2[i], t_hate_3[i], t_hate_1[i]))
    # for i in range(len(t_y)):
    #     print(t_high[i], t_y[i])
    # get_precision(get_class(high), get_class(y))
    # get_precision(get_class(t_high), get_class(t_y))

    '''
    GOAL: LOW
    '''
    model_1 = one_liner_model(0.857, -39.229)
    y = list()
    for x in sad_4:
        y.append(model_1(x))
    t_y = list()
    for i in range(len(t_txt_data)):
        t_y.append(model_1(t_sad_4[i]))
    # for i in range(len(t_y)):
    #     print(t_low[i], t_y[i])
    get_precision(get_class(low), get_class(y))
    get_precision(get_class(t_low), get_class(t_y))

    y = list()
    model_2 = two_liner_model(-3.843, -31.060, 13.369)
    for i in range(len(txt_data)):
        y.append(model_2(sad_4[i], happy_1[i]))
    t_y = list()
    # for i in range(len(t_txt_data)):
    #     t_y.append(model_2(t_sad_4[i], t_happy_1[i]))
    for i in range(len(t_y)):
        print(t_low[i], t_y[i])
    get_precision(get_class(low), get_class(y))
    get_precision(get_class(t_low), get_class(t_y))


def use_div():
    txt_data = np.loadtxt('data/0729_div.txt', float)
    close = txt_data[:, 0]
    div_2_4_4 = txt_data[:, 17]
    div_2_3_2 = txt_data[:, 9]
    print div_2_3_2
    t_txt_data = np.loadtxt('data/test_div.txt', float)
    t_close = t_txt_data[:, 0]
    t_div_2_4_4 = t_txt_data[:, 17]
    t_div_2_3_2 = t_txt_data[:, 9]

    '''
    GOAL: CLOSE
    '''
    model_1 = one_liner_model(-1.922 ,1.204)
    y = list()
    for x in div_2_4_4:
        y.append(model_1(x))
    t_y = list()
    for i in range(len(t_txt_data)):
        t_y.append(model_1(t_div_2_4_4[i]))

    get_precision(get_class(close), get_class(y))
    get_precision(get_class(t_close), get_class(t_y))

    y = list()
    model_2 = two_liner_model(-1.295, 2.386, -1.571)
    for i in range(len(txt_data)):
        # print close[i], div_2_4_4[i], div_2_3_2[i]
        y.append(model_2(div_2_4_4[i], div_2_3_2[i]))
    t_y = list()
    for i in range(len(t_txt_data)):
        # print t_close[i], t_div_2_4_4[i], t_div_2_3_2[i]
        t_y.append(model_2(t_div_2_4_4[i], t_div_2_3_2[i]))

    # for i in range(len(y)):
    #     print(close[i], y[i])
    for i in range(len(t_y)):
        print(t_close[i], t_y[i])
    get_precision(get_class(close), get_class(y))
    get_precision(get_class(t_close), get_class(t_y))

def use_sum():
    txt_data = np.loadtxt('data/0729_sum.txt', float)
    close = txt_data[:, 0]
    high = txt_data[:, 1]
    sum_2 = txt_data[:, 4]
    sum_3 = txt_data[:, 5]

    t_txt_data = np.loadtxt('data/test_sum.txt', float)
    t_close = t_txt_data[:, 0]
    t_high = t_txt_data[:, 1]
    t_sum_2 = t_txt_data[:, 4]
    t_sum_3 = t_txt_data[:, 5]

    model_1 = one_liner_model(0.095, 4.033)
    y = list()
    for x in sum_2:
        y.append(model_1(x))

    t_y = list()
    for i in range(len(t_txt_data)):
        t_y.append(model_1(t_sum_2[i]))

    get_precision(get_class(high), get_class(y))
    get_precision(get_class(t_high), get_class(t_y))

    # 只有比例，及比例和总量，做逐步回归
    y = list()
    model_2 = two_liner_model(0.589, 7.606, -5.293)
    for i in range(len(txt_data)):
        y.append(model_2(sum_2[i], sum_3[i]))

    t_y = list()
    for i in range(len(t_txt_data)):
        t_y.append(model_2(t_sum_2[i], t_sum_3[i]))

    # for i in range(len(y)):
    #     print(close[i], y[i])
    # for i in range(len(t_y)):
    #     print(t_close[i], t_y[i])

    get_precision(get_class(high), get_class(y))
    get_precision(get_class(t_high), get_class(t_y))

def use_stock_word():

    txt_data = np.loadtxt('data/0731_stock.txt', float)
    close = txt_data[:, 0]

    for i in range(1, len(txt_data[0, :])):
        # print close
        # print txt_data[:, i]
        get_precision(get_class(close), get_class(txt_data[:, i]))

def model_close():
    '''
    X: div_fright_4, div_sad_2
    Y: CLOSE
    '''
    return two_liner_model(-1.295, 2.386, -1.571)

def model_high():
    '''
    X: sad_2, disgust_3, disgust_1
    Y: HIGH
    '''
    return thr_liner_model(-0.202, 15.230, 19.308, -15.928)

def model_low():
    '''
    X: sad_4, happy_1
    Y: LOW
    '''
    return two_liner_model(-3.843, -31.060, 13.369)

if __name__ == '__main__':
    # use_bili()
    use_div()
    # use_sum()
    # use_stock_word()