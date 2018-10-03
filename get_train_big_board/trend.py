# -*- coding: utf-8 -*-
__author__ = 'Kay'

# import numpy as np

def get_trend_rise_fall(li):
    '''
    :param li:
    :return: 获取趋势
    '''
    trend = list()
    for i in range(len(li)):
        trend.append( 1 if float(li[i]) >= 0 else 0 )
    return trend

def get_trend(li):
    '''
    :param li:
    :return: 获取趋势
    '''
    trend = list()
    for i in range(1, len(li)):
        trend.append( 1 if float(li[i]) >= float(li[i - 1]) else 0 )
    return trend

def get_precision(li1, li2):
    '''
    :param li1: 真实趋势
    :param li2: 预测趋势
    :return:
    '''
    bingo = 0
    for i in range(len(li1) if len(li1) <= len(li2) else len(li2)):
        if li1[i] == li2[i]:
            bingo += 1
    return bingo / len(li2)

def rise_or_fall(li, threshold, bigger=True):
    result = list()
    for l in li:
        if bigger:
            result.append(1 if float(l) >= threshold else 0)
        else:
            result.append(0 if float(l) >= threshold else 1)

    return result


index = 0
rise_fall = list()
mood_0 = list()
mood_1 = list()
mood_2 = list()
mood_3 = list()
mood_4 = list()
sub = list()
amount = list()

happy = list()
fear = list()

fi = 'data/0726_norm_all.txt'
# fi = 'data/0727_test_norm_all.txt'

for line in open(fi):
    line = line.strip()
    result = line.split(' ')
    rise_fall.append(result[0])
    mood_0.append(result[1])
    mood_1.append(result[2])
    mood_2.append(result[3])
    mood_3.append(result[4])
    mood_4.append(result[5])
    # sub.append(result[6])
    # amount.append(result[7])
    fear.append(result[10])
    happy.append(result[18])

# 遍历预测延迟时间
for i in range(0, 1):

    trend1 = get_trend(rise_fall[i:])
    # trend1 = get_trend_rise_fall(rise_fall[i:])
    # print(len(trend1))
    print(trend1)

    # trend2 = get_trend(fear)
    print(fear)

    # for i in np.linspace(0.3, 1.0, 20):
    #     print('threshold', i)
    #     trend2 = rise_or_fall(fear, i, False)
    #     # print(len(trend2))
    #     # print(trend2)
    #     print(get_precision(trend1, trend2), '\n')

    # trend2 = rise_or_fall(happy, 0.39, True)
    trend2 = get_trend(happy)
    print(len(trend2))
    print(trend2)
    print(get_precision(trend1, trend2))


