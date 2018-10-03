# coding:utf-8
__author__ = 'Kay Zhou'


import datetime
import arrow
import math

import pandas as pd
import tushare as ts

# import count_stock_keyword
import mongo_handler
import time_tool


def get_mood_day(coll, dt):
    """
    获取日期为dt的大盘情绪指数
    """
    return coll.find_one({'_id': 'DY00001' + dt + '2400'}, {'_id': 0, 'mood': 1, 'stat': 1})
    # return coll.find_one({'_id': 'DY00002' + dt + '2400'}, {'_id': 0, 'mood': 1, 'stat': 1})


def get_mood_hour(coll, dt):
    """
    获取日期为dt的大盘情绪指数(小时级别)
    """
    mood_hour_data = []
    for i in range(0, 24):
        mood_hour_data.append(coll.find_one({'_id': 'DY00001%s%s00' % (dt, str(i).zfill(2))}, {'_id': 0, 'mood': 1, 'stat': 1}))
        print('DY00001%s0%s00' % (dt, str(i).zfill(2)))
    print(mood_hour_data)
    return mood_hour_data


def get_mood_close_open(coll, today):
    yest = dec_day(today, 1)
    mood_hour_data = dict()

    for i in range(15, 24):
        mood_hour_data[i] = coll.find_one({'_id': 'DY00001%s%s00' % (yest, str(i))}, {'_id': 0, 'mood': 1, 'stat': 1})

    for i in range(0, 9):
        mood_hour_data[i] = coll.find_one({'_id': 'DY00001%s0%s00' % (today, str(i))}, {'_id': 0, 'mood': 1, 'stat': 1})

    return sum_mood(mood_hour_data)


def get_mood_15_09(coll, today, series):
    yest = dec_trade_day(today, series, 1)
    mood_hour_data = dict()

    for i in range(15, 24):
        mood_hour_data[i] = coll.find_one({'_id': 'DY00001%s%s00' % (yest, str(i))}, {'_id': 0, 'mood': 1, 'stat': 1})

    for i in range(0, 9):
        mood_hour_data[i] = coll.find_one({'_id': 'DY00001%s0%s00' % (today, str(i))}, {'_id': 0, 'mood': 1, 'stat': 1})

    return sum_mood(mood_hour_data)


def get_mood_09_09(coll, today, series):
    yest = dec_trade_day(today, series, 1)
    mood_hour_data = dict()

    for i in range(9, 24):
        mood_hour_data[i] = coll.find_one({'_id': 'DY00001%s%s00' % (yest, str(i))}, {'_id': 0, 'mood': 1, 'stat': 1})

    for i in range(0, 9):
        mood_hour_data[i] = coll.find_one({'_id': 'DY00001%s0%s00' % (today, str(i))}, {'_id': 0, 'mood': 1, 'stat': 1})

    return sum_mood(mood_hour_data)


def get_trade_mood(coll, today):

    mood_hour_data = dict()

    for i in range(8, 15):
        mood_hour_data[i] = coll.find_one({'_id': 'DY00001%s%s00' % (today, str(i))}, {'_id': 0, 'mood': 1, 'stat': 1})

    return sum_mood(mood_hour_data)


def get_mood_series():
    coll = mongo_handler.get_stock_coll()
    dt = '20141201'; end = '20150916'
    while dt <= end:
        di_mood = get_mood_day(coll, dt)
        print(dt, di_mood['mood']['0'], di_mood['mood']['1'], di_mood['mood']['2'],\
                  di_mood['mood']['3'], di_mood['mood']['4'], di_mood['stat']['m_sum'])
        dt = time_tool.add_day_rule(dt, '%Y%m%d')


def dec_day(str_datetime, n, rule='%Y%m%d'):
    '''
    :param str_datetime: 时间字符串
    :return: -1 day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, rule)
    time_delta = datetime.timedelta(days=n)
    dt = dt - time_delta
    return dt.strftime(rule)


def dec_trade_day(str_datetime, series, n, from_='%Y-%m-%d', to='%Y%m%d'):
    '''
    :param str_datetime: 时间字符串
    :return: -n trade_day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, to).strftime(from_)
    index_dec = series.index(dt) - n
    if index_dec < 0:
        print('缺少数据：', dt, n)
        return False

    return datetime.datetime.strptime(series[index_dec], from_).strftime(to)
    # return series[index_dec]


def sum_mood(mood_hour_data):
    '''
    合并大盘小时数据
    '''
    data = {
                'mood':{'0':0, '1':0, '2':0, '3':0, '4':0},
                'stat':{'m_sum': 0}
        }

    for key in mood_hour_data:
        # print(mood_hour_data[key]
        # print(mood_hour_data[key]['mood']
        # print(mood_hour_data[key]['mood']['0']

        # 如果当天没有数据则跳过
        if not mood_hour_data[key]:
            continue
        data['mood']['0'] += mood_hour_data[key]['mood']['0']
        data['mood']['1'] += mood_hour_data[key]['mood']['1']
        data['mood']['2'] += mood_hour_data[key]['mood']['2']
        data['mood']['3'] += mood_hour_data[key]['mood']['3']
        data['mood']['4'] += mood_hour_data[key]['mood']['4']
        data['stat']['m_sum'] += mood_hour_data[key]['stat']['m_sum']

    return data


# 获取大盘交易时间的数据
def write_trade_mood(start, end, out_name):
    coll = mongo_handler.get_stock_coll()
    out = open(out_name, 'w')
    dt = start
    while dt < end:
        print(dt)
        mood = get_trade_mood(coll, dt)['mood']
        out.write(dt + ' ' + str(mood['0']) + ' ' + str(mood['1']) + ' ' + str(mood['2']) + ' '
                     + str(mood['3']) + ' ' + str(mood['4']) + '\n' )
        dt = time_tool.add_day_rule(dt, '%Y%m%d')
    out.close()


# 获取大盘交易时间的数据
def write_mood(start, end, out_name):
    coll = mongo_handler.get_stock_coll()
    out = open(out_name, 'w')
    dt = start
    while dt < end:
        print(dt)
        mood = get_mood_day(coll, dt)['mood']
        out.write(dt + ' ' + str(mood['0']) + ' ' + str(mood['1']) + ' ' + str(mood['2']) + ' '
                     + str(mood['3']) + ' ' + str(mood['4']) + '\n' )
        dt = time_tool.add_day_rule(dt, '%Y%m%d')
    out.close()


def get_big_board_mood_old(fi, fi_train):
    '''
    获取涨跌率及情绪，已经弃用
    '''
    file_train = open(fi_train, 'w')
    coll = mongo_handler.get_stock_coll()
    for line in open(fi):
        dt, extent = line.strip().split(',')
        dt = datetime.datetime.strptime(dt, '%Y/%m/%d').strftime('%Y%m%d')
        dt = dec_day(dt, 1)
        data = get_mood_day(coll, dt)
        if data:
            mood = data['mood']
            m_sum = data['stat']['m_sum']
            y = extent
            x = list()
            x.append(str(float(mood['0']) / m_sum * 10))
            x.append(str(float(mood['1']) / m_sum * 10))
            x.append(str(float(mood['2']) / m_sum * 10))
            x.append(str(float(mood['3']) / m_sum * 10))
            x.append(str(float(mood['4']) / m_sum * 10))
            x.append(str(float(m_sum) / 30000))
            file_train.write(y + '\t' + '\t'.join(x) + '\n')

            # file_train.write(dt + '\t' + extent + '\t' + str(mood['0']) + '\t' + str(mood['1']) + '\t' + str(mood['2']) + '\t'
            #                     + str(mood['3']) + '\t' + str(mood['4']) + '\t' + str(mood['-1']) + '\n')


def get_professional_mood(fi, fi_train):
    '''
    获取涨跌率及情绪，专家经验只使用2、4数据，输出结果为拟合所需，前一天的总量
    '''
    file_train = open(fi_train, 'w')
    coll = mongo_handler.get_stock_coll()
    for line in open(fi):
        dt, extent = line.strip().split(',')
        dt = datetime.datetime.strptime(dt, '%Y/%m/%d').strftime('%Y%m%d')
        print('训练数据获取中：', dt)
        dt = dec_day(dt, 1) # 获取前一天的日期
        data = get_mood_day(coll, dt)

        if data:
            mood = data['mood']
            # m_sum = data['stat']['m_sum']

            # 分类问题
            # y = '1' if float(extent) >= 0.0 else '0'
            # x = list()
            # x.append(str(float(mood['2'])))
            # x.append(str(float(mood['4'])))
            # # file_train.write(y + '\t' + '\t'.join(x) + '\n')
            # file_train.write(y + ' ' + ' '.join([str(i+1) + ':' + str(xi) for i, xi in enumerate(x)]) + '\n')

            # 分类问题
            # y = '1' if float(extent) >= 0.0 else '0'

            #if float(extent) >= 2.0:
            #        y = '1'
            #    elif float(extent) <= -2.0:
            #        y = '-1'
            #    else:
            #        y = '0'
            y = extent
            x = list()
            x.append(str(float(mood['0']) / 1000))
            x.append(str(float(mood['1']) / 1000))
            x.append(str(float(mood['2']) / 1000))
            x.append(str(float(mood['3']) / 1000))
            x.append(str(float(mood['4']) / 1000))
            # file_train.write(y + '\t' + '\t'.join(x) + '\n')
            file_train.write(y + ' ' + ' '.join(x) + '\n')
            # file_train.write(y + ' ' + ' '.join([str(i+1) + ':' + str(xi) for i, xi in enumerate(x)]) + '\n')


def get_mood_last_n(fi, fi_train):
    '''
    获取涨跌率及情绪，前n天的各个情绪数据
    '''
    file_train = open(fi_train, 'w')
    coll = mongo_handler.get_stock_coll()
    is_instruction = True
    for line in open(fi):

        if is_instruction:
            is_instruction = False
            continue

        print(line)
        real_big_board = line.strip().split(',')
        # 日期
        dt = datetime.datetime.strptime(real_big_board[0], '%Y/%m/%d').strftime('%Y%m%d')
        price_close = float(real_big_board[1])
        price_high = float(real_big_board[2])
        price_low = float(real_big_board[3])
        price_open = float(real_big_board[4])
        extent = float(real_big_board[7])

        print('训练数据获取中：', dt)

        def get_last_mood(dt, n):
            '''
            内嵌函数
            获取前n天的情绪数据
            '''
            dt_n = dec_day(dt, n)
            return get_mood_day(coll, dt_n)

        # 涨跌幅作为预测目标
        # if abs(extent) > 5.0: continue
        y = str(extent)

        # 报告中的公式作为预测目标
        # y = str(math.log(price_close) - math.log(price_open))

        x = list()

        # 获取前n(7)天的数据，并且进行预处理
        for i in range(1, 2):
            # mood = get_last_mood(dt, i)['mood']
            # granger revise
            mood = get_mood_day(coll, dt)['mood']

            m_sum = get_last_mood(dt, i)['stat']['m_sum']

            # 情绪注释
            # print(count, i, '情绪0'; count += 1
            # print(count, i, '情绪1'; count += 1
            # print(count, i, '情绪2'; count += 1
            # print(count, i, '情绪3'; count += 1
            # print(count, i, '情绪4'; count += 1
            # print(count, i, '总量'; count += 1
            # print(count, i, '比例0'; count += 1
            # print(count, i, '比例1'; count += 1
            # print(count, i, '比例2'; count += 1
            # print(count, i, '比例3'; count += 1
            # print(count, i, '比例4'; count += 1

            # 绝对情绪
            x.append(str(float(mood['0']) / 10000))
            x.append(str(float(mood['1']) / 10000))
            x.append(str(float(mood['2']) / 10000))
            x.append(str(float(mood['3']) / 10000))
            x.append(str(float(mood['4']) / 10000))

            # 取Log
            # x.append(str(math.log(float(mood['0']))))
            # x.append(str(math.log(float(mood['1']))))
            # x.append(str(math.log(float(mood['2']))))
            # x.append(str(math.log(float(mood['3']))))
            # x.append(str(math.log(float(mood['4']))))

            # 数据总和及情绪比例
            # x.append(str(float(m_sum) / 10000))
            # x.append(str(float(mood['0']) / float(m_sum)))
            # x.append(str(float(mood['1']) / float(m_sum)))
            # x.append(str(float(mood['2']) / float(m_sum)))
            # x.append(str(float(mood['3']) / float(m_sum)))
            # x.append(str(float(mood['4']) / float(m_sum)))

        # break
        file_train.write(y + ' ' + ' '.join(x) + '\n')


def get_date_series(fi):
    '''
    :param fi: 大盘数据
    :return: 日期序列
    '''
    dt_series = list()
    # warning
    # dt_series = ['2015/6/30', '2015/7/1', '2015/7/2', '2015/7/3', '2015/7/6']
    is_instruction = True

    for line in open(fi):
        if is_instruction:
            is_instruction = False
            continue
        dt_series.append(line.split(',')[0])

    # print(dt_series)
    return dt_series


def get_train_data_from_csv(fi, fi_train):
    '''ls
    获取收盘数据，前n天的各个情绪数据
    '''
    file_train = open(fi_train, 'w')
    coll = mongo_handler.get_stock_coll()
    is_instruction = True

    # 取得时间序列
    series = get_date_series(fi)

    for line in open(fi):

        if is_instruction:
            is_instruction = False
            continue

        print(line)
        real_big_board = line.strip().split(',')

        # 日期
        # dt = datetime.datetime.strptime(real_big_board[0], '%Y/%m/%d').strftime('%Y%m%d')

        # 日期及真实数据
        today = real_big_board[0]
        price_close = float(real_big_board[1])
        price_high = float(real_big_board[2])
        price_low = float(real_big_board[3])
        price_open = float(real_big_board[4])
        extent_yesterday = float(real_big_board[5])
        extent = float(real_big_board[7])
        amount = float(real_big_board[8])
        sum_money = float(real_big_board[9])

        # 涨跌幅当日最大最小
        extent_open = (price_open - extent_yesterday) / extent_yesterday * 100
        extent_high = (price_high - extent_yesterday) / extent_yesterday * 100
        extent_low = (price_low - extent_yesterday) / extent_yesterday * 100

        print('训练数据获取中：', today)

        def get_last_mood(dt, n):
            '''
            内嵌函数
            获取前n天的情绪数据
            '''
            print(dt, n)
            dt_n = dec_day(dt, n)
            return get_mood_day(coll, dt_n)

        y = list()
        # y.append(price_close)
        # y.append(price_open)
        # y.append(price_high)
        # y.append(price_low)

        # y.append(today)

        # 收盘价作为预测目标
        # y = str(price_close)

        # 涨跌幅作为预测目标
        # if abs(extent) > 5.0: continue
        # y.append(str(extent))
        y.append('1' if extent > 0 else '0')
        # y = '1' if extent > 0 else '0'

        # 报告中的公式作为预测目标
        # y = str(math.log(price_close) - math.log(price_open))

        # 其它标准
        # y.append(str(extent_high))
        # y.append(str(extent_low))

        y.append('1' if extent_open > 0 else '0')
        # y.append('%.4f' % (extent_open))
        y.append('%.4f' % (extent_high))
        y.append('%.4f' % (extent_low))
        y.append(str(amount))

        x = list()

        for i in range(1, 6):  # 获取前n天的数据，并且进行预处理
        # for i in range(0, 1): # 格兰杰
            # 获取训练数据日期
            train_date = dec_trade_day(today, series, i)
            if train_date == False:
                break
            print('训练数据日期：', train_date)

            try:
                # 一天数据
                doc = get_mood_day(coll, train_date)
                # 交易时段的数据
                # doc = get_trade_mood(coll, train_date)

                mood = doc['mood']
                m_sum = doc['stat']['m_sum']

            except TypeError:
                break

            # 绝对情绪
            # x.append(str(float(mood['0']) / 4800))
            # x.append(str(float(mood['1']) / 4900))
            # x.append(str(float(mood['2']) / 9700))
            # x.append(str(float(mood['3']) / 2500))
            # x.append(str(float(mood['4']) / 10200))
            # x.append(str(m_sum))

            # 绝对情绪修正
            # x.append(str(float(mood['0']) / 1000))
            # x.append(str(float(mood['1']) / 1000))
            # x.append(str(float(mood['2']) / 1000))
            # x.append(str(float(mood['3']) / 1000))
            # x.append(str(float(mood['4']) / 1000))

            # 绝对情绪，取Log
            # x.append(str(math.log(float(mood['0']))))
            # x.append(str(math.log(float(mood['1']))))
            # x.append(str(math.log(float(mood['2']))))
            # x.append(str(math.log(float(mood['3']))))
            # x.append(str(math.log(float(mood['4']))))

            # 数据总和及情绪比例
            # x.append(str(float(m_sum) / 100000))

            # 总量
            # five_sum = float(mood['0']) + float(mood['1']) + float(mood['2']) + float(mood['3']) + float(mood['4'])
            # x.append(str(float(mood['0']) / five_sum))
            # x.append(str(float(mood['1']) / five_sum))
            # x.append(str(float(mood['2']) / five_sum))
            # x.append(str(float(mood['3']) / five_sum))
            # x.append(str(float(mood['4']) / five_sum))

            # 保留小数点后两位
            # x.append('%.4f' % (float(mood['0']) / five_sum))
            # x.append('%.4f' % (float(mood['1']) / five_sum))
            # x.append('%.4f' % (float(mood['2']) / five_sum))
            # x.append('%.4f' % (float(mood['3']) / five_sum))
            # x.append('%.4f' % (float(mood['4']) / five_sum))

            # x.append(str(float(mood['0']) / float(m_sum)))
            # x.append(str(float(mood['1']) / float(m_sum)))
            # x.append(str(float(mood['2']) / float(m_sum)))
            # x.append(str(float(mood['3']) / float(m_sum)))
            # x.append(str(float(mood['4']) / float(m_sum)))

            # 各种组合情绪，差值
            # x.append( str(float(mood['2']) - float(mood['0'])) )
            # x.append( str(float(mood['2']) - float(mood['1'])) )
            # x.append( str(float(mood['2']) - float(mood['3'])) )
            # x.append( str(float(mood['2']) - float(mood['4'])) )

            # 比值
            x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['0'])))) )
            x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['1'])))) )
            x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['2'])))) )
            x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['3'])))) )
            x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['4'])))) )

            # 成交量与成交金额，取Log
            # x.append(str(math.log(amount)))
            # x.append(str(math.log(sum_money)))

        else:
            # 将训练数据写入到文件
            file_train.write(' '.join(y) + ' ' + ' '.join(x) + '\n')
            # file_train.write(y + '\t' + '\t'.join([str(i+1) + ':' + str(xi) for i, xi in enumerate(x)]) + '\n')


def get_real_data_file(fi, fi_train):
    '''
    获取收盘数据，及当天情绪
    '''
    file_train = open(fi_train, 'w')
    coll = mongo_handler.get_stock_coll()
    is_instruction = True

    # 取得时间序列
    series = get_date_series(fi)

    for line in open(fi):

        if is_instruction:
            is_instruction = False
            continue

        print(line)
        real_big_board = line.strip().split(',')

        # 日期
        # dt = datetime.datetime.strptime(real_big_board[0], '%Y/%m/%d').strftime('%Y%m%d')

        # 日期及真实数据
        # today = real_big_board[0]
        today = datetime.datetime.strptime(real_big_board[0], '%Y/%m/%d').strftime('%Y%m%d')
        price_close = float(real_big_board[1])
        price_high = float(real_big_board[2])
        price_low = float(real_big_board[3])
        price_open = float(real_big_board[4])
        extent_yesterday = float(real_big_board[5])
        extent = float(real_big_board[7])
        amount = float(real_big_board[8])
        sum_money = float(real_big_board[9])

        # 涨跌幅当日最大最小
        extent_high = (price_high - extent_yesterday) / extent_yesterday * 100
        extent_low = (price_low - extent_yesterday) / extent_yesterday * 100

        print('训练数据获取中：', today)

        y = list()
        y = [real_big_board[0]]
        # y.append(str(extent))
        # y.append(str(extent_high))
        # y.append(str(extent_low))

        x = list()
        doc = get_mood_day(coll, today)

        if not doc:
            print(today, doc)
            continue

        mood = doc['mood']
        m_sum = doc['stat']['m_sum']

        # 绝对情绪
        x.append(str(float(mood['0'])))
        x.append(str(float(mood['1'])))
        x.append(str(float(mood['2'])))
        x.append(str(float(mood['3'])))
        x.append(str(float(mood['4'])))
        x.append(str(m_sum))

        # file_train.write(' '.join(x) + '\n')
        file_train.write('\t'.join(y) + '\t' + '\t'.join(x) + '\n')


def get_train_stock_keyword(fi, fi_train):
    '''
    获取涨跌率及情绪，stock_keyword = [u'涨', u'跌', u'买', u'卖']，四个关键词出现的次数作为预测输入
    '''
    file_train = open(fi_train, 'w')
    cnts = count_stock_keyword.load_count_stock_keyword()

    # 取得时间序列
    series = get_date_series(fi)

    is_instruction = True

    for line in open(fi):

        if is_instruction:
            is_instruction = False
            continue

        real_big_board = line.strip().split(',')

        # 日期及真实数据
        today = real_big_board[0]
        price_close = float(real_big_board[1])
        price_high = float(real_big_board[2])
        price_low = float(real_big_board[3])
        price_open = float(real_big_board[4])
        extent_yesterday = float(real_big_board[5])
        extent = float(real_big_board[7])
        amount = float(real_big_board[8])
        sum_money = float(real_big_board[9])

        # today = datetime.datetime.strptime(today, '%Y/%m/%d').strftime('%Y%m%d')

        print('训练数据获取中：', today)

        def datetime_magic(str_dt, rule1, rule2):
            return datetime.datetime.strptime(str_dt, rule1).strftime(rule2)

        # 异常情况处理
        # if abs(float(extent)) > 5.0:
        #     print('异常情况处理:', extent)
        #     continue

        x = list()
        index_bullish = extent

        for i in range(1, 6): # 可选择天数
            # print(i)
            try:
                train_date = dec_trade_day(today, series, i)
                if not train_date: break
                cnt_data = cnts[datetime_magic(train_date, '%Y%m%d', '%Y-%m-%d')]
            except KeyError:
                print('缺失数据。')
                break

            # 涨 / 跌
            # x.append(float(cnt_data[0]) / float(cnt_data[1]))
            x.append(math.log((1 + float(cnt_data[0])) / (1 + float(cnt_data[1]))))

            # 买 / 卖
            # x.append(float(cnt_data[2]) / float(cnt_data[3]))
            x.append(math.log((1 + float(cnt_data[2])) / (1 + float(cnt_data[3]))))

        else:
            file_train.write(str(index_bullish) + ' ' + ' '.join([str(xi) for xi in x]) + '\n')

def deal_with_x(x):
    '''
    比例与总量
    '''
    x_new = [0.0] * 6
    for i in range(5):
        x_new[i] = float(x[i]) / float(x[5]) * 10
    x_new[5] = float(x[5]) / 10000
    return x_new


def get_big_board_mood(fi, fi_train):
    '''
    获取涨跌率及情绪，收盘后及开盘前
    '''
    file_train = open(fi_train, 'w')
    coll = mongo_handler.get_stock_coll()
    for line in open(fi):
        dt, extent = line.strip().split(',')
        dt = datetime.strptime(dt, '%Y/%m/%d').strftime('%Y%m%d')
        data = get_mood_close_open(coll, dt)
        if data:
            print(data)
            x = deal_with_x(data)
            y = extent
            # y = '1' if float(extent) >= 0.0 else '0'
            print(y)
            file_train.write(y + '\t' + '\t'.join([str(xi) for xi in x]) + '\n')
            # file_train.write(y + '\t' + '\t'.join([str(i+1) + ':' + str(xi) for i, xi in enumerate(x)]) + '\n')


def get_train_data(start, end, out_name):
    '''
    获取收盘数据，前n天的各个情绪数据，真实交易数据是由tushare获取
    '''

    # 获取真实大盘数据
    results = ts.get_hist_data('sh', start=start, end=end)
    print('成功获取 -> 历史大盘数据 ... ...')

    # 取得时间序列
    series = list(results.index)
    print(series)

    # 获取数据库连接
    coll = mongo_handler.get_stock_coll()

    # 遍历每天交易实际数据
    for i, date in enumerate(series):
        # 第一天留出
        if i == 0: continue

        # 日期及真实数据
        today = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
        price_close = results.loc[date]['close']
        price_open = results.loc[date]['open']
        price_high = results.loc[date]['high']
        price_low = results.loc[date]['low']
        volume = results.loc[date]['volume'] * 100
        last_close = results.loc[series[i-1]]['close']
        extent = results.loc[date]['p_change']

        # 涨跌幅当日最大最小
        extent_open = (price_open - last_close) / last_close * 100
        extent_high = (price_high - last_close) / last_close * 100
        extent_low = (price_low - last_close) / last_close * 100

        # 创造目标函数
        y = list()
        # y.append(today)
        y.append(date)

        # 收盘价作为预测目标
        y.append(str(price_close))

        # 涨跌幅作为预测目标
        # if abs(extent) > 5.0: continue
        # y.append(str(extent))
        # y.append(str(price_close))
        # y.append('1' if extent > 0 else '0')
        # y = '1' if extent > 0 else '0'

        # 报告中的公式作为预测目标
        # y = str(math.log(price_close) - math.log(price_open))

        # 其它标准
        # y.append(str(extent_high))
        # y.append(str(extent_low))

        # y.append('1' if extent_open > 0 else '0')
        y.append('%.4f' % (extent))
        y.append('%.4f' % (extent_open))
        y.append('%.4f' % (extent_high))
        y.append('%.4f' % (extent_low))

        y.append(str(volume))

        def get_last_mood(dt, n):
            '''
            内嵌函数
            获取前n天的情绪数据
            '''
            print(dt, n)
            dt_n = dec_day(dt, n)
            return get_mood_day(coll, dt_n)

        x = list()

        print('训练数据获取中：', today)

        # for i in range(1, 21):  # 获取前n天的数据，并且进行预处理
        for i in range(0, 1): # 格兰杰, 取当天数据
            # 获取训练数据日期
            train_date = dec_trade_day(today, series, i)
            if train_date == False: break
            print('训练数据日期：', train_date)

            try:
                # 一天数据
                doc = get_mood_day(coll, train_date)

                # 非交易时段的数据
                # doc = get_mood_15_09(coll, train_date, series)

                mood = doc['mood']
                m_sum = doc['stat']['m_sum']

            except TypeError:
                break

            # 绝对情绪
            x.append(str(float(mood['0'])))
            x.append(str(float(mood['1'])))
            x.append(str(float(mood['2'])))
            x.append(str(float(mood['3'])))
            x.append(str(float(mood['4'])))
            x.append(str(m_sum))

            # 绝对情绪，取Log
            # x.append(str(math.log(float(mood['0']))))
            # x.append(str(math.log(float(mood['1']))))
            # x.append(str(math.log(float(mood['2']))))
            # x.append(str(math.log(float(mood['3']))))
            # x.append(str(math.log(float(mood['4']))))

            # 数据总和及情绪比例
            # x.append(str(float(m_sum) / 100000))

            # 总量
            # five_sum = float(mood['0']) + float(mood['1']) + float(mood['2']) + float(mood['3']) + float(mood['4'])
            # x.append(str(float(mood['0']) / five_sum))
            # x.append(str(float(mood['1']) / five_sum))
            # x.append(str(float(mood['2']) / five_sum))
            # x.append(str(float(mood['3']) / five_sum))
            # x.append(str(float(mood['4']) / five_sum))

            # 保留小数点后两位
            # x.append('%.4f' % (float(mood['0']) / five_sum))
            # x.append('%.4f' % (float(mood['1']) / five_sum))
            # x.append('%.4f' % (float(mood['2']) / five_sum))
            # x.append('%.4f' % (float(mood['3']) / five_sum))
            # x.append('%.4f' % (float(mood['4']) / five_sum))

            # x.append(str(float(mood['0']) / float(m_sum)))
            # x.append(str(float(mood['1']) / float(m_sum)))
            # x.append(str(float(mood['2']) / float(m_sum)))
            # x.append(str(float(mood['3']) / float(m_sum)))
            # x.append(str(float(mood['4']) / float(m_sum)))

            # 各种组合情绪，差值
            # x.append( str(float(mood['2']) - float(mood['0'])) )
            # x.append( str(float(mood['2']) - float(mood['1'])) )
            # x.append( str(float(mood['2']) - float(mood['3'])) )
            # x.append( str(float(mood['2']) - float(mood['4'])) )

            # 比值
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['0'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['1'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['2'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['3'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['4'])))) )

            # 成交量与成交金额，取Log
            # x.append(str(math.log(amount)))
            # x.append(str(math.log(sum_money)))

        else:
            # 将训练数据写入到文件
            file_train = open(out_name, 'a')
            file_train.write(','.join(y) + ',' + ','.join(x) + '\n')
            print(' '.join(y) + ' ' + ' '.join(x))
            # file_train.write(y + '\t' + '\t'.join([str(i+1) + ':' + str(xi) for i, xi in enumerate(x)]) + '\n')


def get_train_data_hour(start, end, out_name):
    '''
    获取收盘数据，前n天的各个情绪数据，真实交易数据是由tushare获取
    '''

    # 获取真实大盘数据
    results = ts.get_hist_data('sh', start=start, end=end)
    print('成功获取 -> 历史大盘数据 ... ...')

    # 取得时间序列
    series = list(results.index)
    print(series)

    # 获取数据库连接
    coll = mongo_handler.get_stock_coll()

    # 遍历每天交易实际数据
    for i, date in enumerate(series):
        # 第一天留出
        if i == 0: continue

        # 日期及真实数据
        today = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
        price_close = results.loc[date]['close']
        price_open = results.loc[date]['open']
        price_high = results.loc[date]['high']
        price_low = results.loc[date]['low']
        volume = results.loc[date]['volume'] * 100
        last_close = results.loc[series[i-1]]['close']
        extent = results.loc[date]['p_change']

        # 涨跌幅当日最大最小
        extent_open = (price_open - last_close) / last_close * 100
        extent_high = (price_high - last_close) / last_close * 100
        extent_low = (price_low - last_close) / last_close * 100

        # 创造目标函数
        y = list()
        # y.append(today)
        y.append(date)

        # 收盘价作为预测目标
        y.append(str(price_close))

        # 涨跌幅作为预测目标
        # if abs(extent) > 5.0: continue
        # y.append(str(extent))
        # y.append(str(price_close))
        # y.append('1' if extent > 0 else '0')
        # y = '1' if extent > 0 else '0'

        # 报告中的公式作为预测目标
        # y = str(math.log(price_close) - math.log(price_open))

        # 其它标准
        # y.append(str(extent_high))
        # y.append(str(extent_low))

        # y.append('1' if extent_open > 0 else '0')
        y.append('%.4f' % (extent))
        y.append('%.4f' % (extent_open))
        y.append('%.4f' % (extent_high))
        y.append('%.4f' % (extent_low))

        y.append(str(volume))

        def get_last_mood(dt, n):
            '''
            内嵌函数
            获取前n天的情绪数据
            '''
            print(dt, n)
            dt_n = dec_day(dt, n)
            return get_mood_day(coll, dt_n)

        x = []

        print('训练数据获取中：', today)

        # for i in range(1, 21):  # 获取前n天的数据，并且进行预处理
        for i in range(0, 1): # 格兰杰, 取当天数据
            # 获取训练数据日期
            train_date = dec_trade_day(today, series, i)
            if train_date == False: break
            print('训练数据日期：', train_date)

            try:
                # 一天数据
                docs = get_mood_hour(coll, train_date)

            except TypeError:
                break

            for doc in docs:
                mood = doc['mood']
                m_sum = doc['stat']['m_sum']
                # 绝对情绪
                x.append(str(float(mood['0'])))
                x.append(str(float(mood['1'])))
                x.append(str(float(mood['2'])))
                x.append(str(float(mood['3'])))
                x.append(str(float(mood['4'])))
                x.append(str(float(m_sum)))
                # five_sum = float(mood['0']) + float(mood['1']) + float(mood['2']) + float(mood['3']) + float(mood['4'])
                # x.append(str(five_sum))

                # 绝对情绪修正
                # x.append(str(float(mood['0']) / 1000))
                # x.append(str(float(mood['1']) / 1000))
                # x.append(str(float(mood['2']) / 1000))
                # x.append(str(float(mood['3']) / 1000))
                # x.append(str(float(mood['4']) / 1000))

                # 绝对情绪，取Log
                # x.append(str(math.log(float(mood['0']))))
                # x.append(str(math.log(float(mood['1']))))
                # x.append(str(math.log(float(mood['2']))))
                # x.append(str(math.log(float(mood['3']))))
                # x.append(str(math.log(float(mood['4']))))

                # 数据总和及情绪比例
                # x.append(str(float(m_sum) / 100000))

                # 总量
                # five_sum = float(mood['0']) + float(mood['1']) + float(mood['2']) + float(mood['3']) + float(mood['4'])
                # x.append(str(float(mood['0']) / five_sum))
                # x.append(str(float(mood['1']) / five_sum))
                # x.append(str(float(mood['2']) / five_sum))
                # x.append(str(float(mood['3']) / five_sum))
                # x.append(str(float(mood['4']) / five_sum))

                # 保留小数点后两位
                # x.append('%.4f' % (float(mood['0']) / five_sum))
                # x.append('%.4f' % (float(mood['1']) / five_sum))
                # x.append('%.4f' % (float(mood['2']) / five_sum))
                # x.append('%.4f' % (float(mood['3']) / five_sum))
                # x.append('%.4f' % (float(mood['4']) / five_sum))

                # x.append(str(float(mood['0']) / float(m_sum)))
                # x.append(str(float(mood['1']) / float(m_sum)))
                # x.append(str(float(mood['2']) / float(m_sum)))
                # x.append(str(float(mood['3']) / float(m_sum)))
                # x.append(str(float(mood['4']) / float(m_sum)))

                # 各种组合情绪，差值
                # x.append( str(float(mood['2']) - float(mood['0'])) )
                # x.append( str(float(mood['2']) - float(mood['1'])) )
                # x.append( str(float(mood['2']) - float(mood['3'])) )
                # x.append( str(float(mood['2']) - float(mood['4'])) )

                # 比值
                # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['0'])))) )
                # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['1'])))) )
                # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['2'])))) )
                # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['3'])))) )
                # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['4'])))) )

                # 成交量与成交金额，取Log
                # x.append(str(math.log(amount)))
                # x.append(str(math.log(sum_money)))

        else:
            # 将训练数据写入到文件
            file_train = open(out_name, 'a')
            file_train.write(','.join(y) + ',' + ','.join(x) + '\n')
            print(','.join(y) + ',' + ','.join(x))
            # file_train.write(y + '\t' + '\t'.join([str(i+1) + ':' + str(xi) for i, xi in enumerate(x)]) + '\n')


def get_prediction_real_data(start, end, out_name):
    '''
    测评预测结果
    '''

    # 获取真实大盘数据
    results = ts.get_hist_data('sh', start=start, end=end)
    print('成功获取 -> 历史大盘数据 ... ...')

    # 取得时间序列
    series = list(results.index)
    print(series)

    # 获取数据库连接
    coll = mongo_handler.get_stock_coll()
    prediction_coll = mongo_handler.get_prediction_coll()

    # 遍历每天交易实际数据
    for i, date in enumerate(series):
        # 第一天留出
        if i == 0: continue

        # 日期及真实数据
        today = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%Y%m%d')
        price_close = results.loc[date]['close']
        price_open = results.loc[date]['open']
        price_high = results.loc[date]['high']
        price_low = results.loc[date]['low']
        volume = results.loc[date]['volume'] * 100
        last_close = results.loc[series[i-1]]['close']
        extent = results.loc[date]['p_change']

        # 涨跌幅当日最大最小
        extent_open = (price_open - last_close) / last_close * 100
        extent_high = (price_high - last_close) / last_close * 100
        extent_low = (price_low - last_close) / last_close * 100

        # 创造目标函数
        y = list()
        y.append(today)

        # 收盘价作为预测目标
        # y = str(price_close)

        # 涨跌幅作为预测目标
        # if abs(extent) > 5.0: continue
        # y.append(str(extent))
        # y.append(str(price_close))
        # y.append('1' if extent > 0 else '0')
        # y = '1' if extent > 0 else '0'

        # 报告中的公式作为预测目标
        # y = str(math.log(price_close) - math.log(price_open))

        # 其它标准
        # y.append(str(extent_high))
        # y.append(str(extent_low))

        # y.append('1' if extent_open > 0 else '0')
        y.append('%.4f' % (extent))
        # y.append('%.4f' % (extent_open))
        y.append('%.4f' % (extent_high))
        y.append('%.4f' % (extent_low))

        # y.append(str(volume))

        # 获取预测数据
        prediction_result = prediction_coll.find_one({'_id': today}, {'_id':0})
        if not prediction_result:
            continue
        pre_close = prediction_result['model_1']['close']
        pre_high = prediction_result['model_1']['high']
        pre_low = prediction_result['model_1']['low']

        y.append('%.4f' % (pre_close))
        y.append('%.4f' % (pre_high))
        y.append('%.4f' % (pre_low))

        # 收盘方向相同
        if (extent * pre_close) > 0:
            y.append('1')
        else:
            y.append('0')

        # 数值出现
        if pre_close >= extent_low and pre_close <= extent_high:
            y.append('1')
        else:
            y.append('0')

        # 最高点方向
        if (extent_high * pre_high) > 0:
            y.append('1')
        else:
            y.append('0')

        # 最低点方向
        if (extent_low * pre_low) > 0:
            y.append('1')
        else:
            y.append('0')

        def get_last_mood(dt, n):
            '''
            内嵌函数
            获取前n天的情绪数据
            '''
            print(dt, n)
            dt_n = dec_day(dt, n)
            return get_mood_day(coll, dt_n)

        x = list()

        print('训练数据获取中：', today)

        # for i in range(6):  # 获取前5天的数据，并且进行预处理
        for i in range(1): # 格兰杰, 只取当日
            # 获取训练数据日期
            train_date = dec_trade_day(today, series, i)
            if train_date == False: break
            print('训练数据日期：', train_date)

            try:
                # 一天数据
                doc = get_mood_day(coll, train_date)

                # 交易时段的数据
                # doc = get_mood_15_09(coll, train_date, series)

                mood = doc['mood']
                # m_sum = doc['stat']['m_sum']

            except TypeError:
                break

            # 绝对情绪
            x.append(str(float(mood['0'])))
            x.append(str(float(mood['1'])))
            x.append(str(float(mood['2'])))
            x.append(str(float(mood['3'])))
            x.append(str(float(mood['4'])))
            # x.append(str(m_sum))

            # 绝对情绪修正
            # x.append(str(float(mood['0']) / 1000))
            # x.append(str(float(mood['1']) / 1000))
            # x.append(str(float(mood['2']) / 1000))
            # x.append(str(float(mood['3']) / 1000))
            # x.append(str(float(mood['4']) / 1000))

            # 绝对情绪，取Log
            # x.append(str(math.log(float(mood['0']))))
            # x.append(str(math.log(float(mood['1']))))
            # x.append(str(math.log(float(mood['2']))))
            # x.append(str(math.log(float(mood['3']))))
            # x.append(str(math.log(float(mood['4']))))

            # 数据总和及情绪比例
            # x.append(str(float(m_sum) / 100000))

            # 总量
            five_sum = float(mood['0']) + float(mood['1']) + float(mood['2']) + float(mood['3']) + float(mood['4'])
            x.append(str(float(mood['0']) / five_sum))
            x.append(str(float(mood['1']) / five_sum))
            x.append(str(float(mood['2']) / five_sum))
            x.append(str(float(mood['3']) / five_sum))
            x.append(str(float(mood['4']) / five_sum))

            # 保留小数点后两位
            # x.append('%.4f' % (float(mood['0']) / five_sum))
            # x.append('%.4f' % (float(mood['1']) / five_sum))
            # x.append('%.4f' % (float(mood['2']) / five_sum))
            # x.append('%.4f' % (float(mood['3']) / five_sum))
            # x.append('%.4f' % (float(mood['4']) / five_sum))

            # x.append(str(float(mood['0']) / float(m_sum)))
            # x.append(str(float(mood['1']) / float(m_sum)))
            # x.append(str(float(mood['2']) / float(m_sum)))
            # x.append(str(float(mood['3']) / float(m_sum)))
            # x.append(str(float(mood['4']) / float(m_sum)))

            # 各种组合情绪，差值
            # x.append( str(float(mood['2']) - float(mood['0'])) )
            # x.append( str(float(mood['2']) - float(mood['1'])) )
            # x.append( str(float(mood['2']) - float(mood['3'])) )
            # x.append( str(float(mood['2']) - float(mood['4'])) )

            # 比值
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['0'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['1'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['2'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['3'])))) )
            # x.append( str( math.log((1 + float(mood['2'])) / (1 + float(mood['4'])))) )

            # 成交量与成交金额，取Log
            # x.append(str(math.log(amount)))
            # x.append(str(math.log(sum_money)))

        else:
            # 将训练数据写入到文件
            open(out_name, 'a').write(','.join(y) + ',' + ','.join(x) + '\n')
            # print(' '.join(y) + ' ' + ' '.join(x))
            # file_train.write(y + '\t' + '\t'.join([str(i+1) + ':' + str(xi) for i, xi in enumerate(x)]) + '\n')

def get_real_data(start, end, out_name):
    '''
    获取收盘数据，前n天的各个情绪数据，真实交易数据是由tushare获取
    '''

    # 获取真实大盘数据
    results = ts.get_hist_data('sh', start=start, end=end)

    # 取得时间序列
    series = list(results.index)

    # 遍历每天交易实际数据
    for i, date in enumerate(series):
        if i == 0: continue

        # 日期及真实数据
        today = date
        price_close = results.loc[date]['close']
        price_open = results.loc[date]['open']
        price_high = results.loc[date]['high']
        price_low = results.loc[date]['low']
        volume = results.loc[date]['volume']
        last_close = results.loc[series[i-1]]['close']
        extent = results.loc[date]['p_change']

        # 涨跌幅当日最大最小
        extent_open = (price_open - last_close) / last_close * 100
        extent_high = (price_high - last_close) / last_close * 100
        extent_low = (price_low - last_close) / last_close * 100

        # 创造目标函数
        y = list()
        y.append(date)

        # 收盘价作为预测目标
        # y = str(price_close)

        # 涨跌幅作为预测目标
        # if abs(extent) > 5.0: continue
        y.append(str(price_close))
        y.append(str(extent))
        # y.append('1' if extent > 0 else '0')
        # y = '1' if extent > 0 else '0'

        # 报告中的公式作为预测目标
        # y = str(math.log(price_close) - math.log(price_open))

        # 其它标准
        # y.append(str(extent_high))
        # y.append(str(extent_low))

        # y.append('1' if extent_open > 0 else '0')

        y.append('%.4f' % (extent_open))
        y.append('%.4f' % (extent_high))
        y.append('%.4f' % (extent_low))
        y.append(str(volume * 100))

        # 将训练数据写入到文件
        file_train = open(out_name, 'a')
        file_train.write('\t'.join(y) + '\n')


def get_emotion(start, end, out_name):
    '''
    获取情绪数据, 按天
    :param start:
    :param end:
    :param out_name:
    :return:
    '''
    out_file = open(out_name, 'w')
    dt = start
    coll = mongo_handler.get_stock_coll()
    title = ['date', 'anger', 'disgust', 'joy', 'sadness', 'fear', 'volume']
    out_file.write(','.join(title) + '\n')
    while dt <= end:
        print(dt)
        x = [dt[:4] + '-' + dt[4:6] + '-' + dt[6:]]
        # x = [dt[4:6] + '-' + dt[6:]]
        data = get_mood_day(coll, dt)
        try:
            mood = data['mood']
        except:
            print('ERROR:', "mood = data['mood']")
            print(data)
            break

        try:
            amount = data['stat']['m_sum']
        except:
            amount = float(mood['0']) + float(mood['1']) + float(mood['2']) + float(mood['3']) + float(mood['4'])

        x.append(str(float(mood['0'])))
        x.append(str(float(mood['1'])))
        x.append(str(float(mood['2'])))
        x.append(str(float(mood['3'])))
        x.append(str(float(mood['4'])))
        
        x.append(str(float(amount)))
        out_file.write(','.join(x) + '\n')
        dt = time_tool.add_day_rule(dt, '%Y%m%d')
        

    out_file.close()


def get_emotion_hour(start, end, out_name):
    '''
    :param start:
    :param end:
    :param out_name:
    :return:
    '''
    out_file = open(out_name, 'w')
    dt = start
    coll = mongo_handler.get_stock_coll()
    title = ['date', 'anger', 'disgust', 'joy', 'sadness', 'fear', 'sum']
    out_file.write(','.join(title) + '\n')
    while dt <= end:
        print(dt)
        docs = get_mood_hour(coll, dt)
        hour = 0
        for doc in docs:
            x = ['{}-{}-{} {}'.format(dt[:4], dt[4:6], dt[6:], hour)]
            mood = doc['mood']
            try:
                m_sum = doc['stat']['m_sum']
            except:
                m_sum = float(mood['0']) + float(mood['1']) + float(mood['2']) + float(mood['3']) + float(mood['4']) 
            # 绝对情绪
            x.append(str(float(mood['0'])))
            x.append(str(float(mood['1'])))
            x.append(str(float(mood['2'])))
            x.append(str(float(mood['3'])))
            x.append(str(float(mood['4'])))
            x.append(str(float(m_sum)))
            out_file.write(','.join(x) + '\n')
            hour += 1
        dt = time_tool.add_day_rule(dt, '%Y%m%d')


def get_train_from_history(out_name):
    '''
    从 20141201-20160501_hour_mood.csv 根据需求提取训练数据
    这是一个善变的函数, 会根据需要经常发生变化 !!!
    :return:
    '''
    data = pd.read_csv('20141201-20160501_hour_mood.csv')
    # data = data[10: 20]

    # 选择延迟天数
    day_lags = 10

    # 选择小时数
    hours = [str(h).zfill(2) for h in list(range(24))]

    # 选择情绪
    emotions = ['anger', 'disgust', 'joy', 'sadness', 'fear']

    for i in list(range(day_lags, data.shape[0])):
        X = []
        for j in range(i - day_lags, i):
            # i 指当日的下标, j 指提前后的下标
            # target = str(data['close'][i])
            target = '1' if data['close'][i] > 0 else '0'
            for h in hours:
                for e in emotions:
                    X.append(str(data[e + h][j]))
        open(out_name,'w').write(target + ',' + ','.join(X) + '\n')



if __name__ == '__main__':
    # 获取真实大盘数据
    # get_real_data('2014-12-01', '2016-12-16', 'real-20141201-20161216.txt')

    # 获取情绪数据
    # get_emotion('20170601', '20170622', 'data/stock_emotions-201706.csv')
    get_emotion_hour('20170601', '20170621', 'data/stock_emotions-hour-201706.csv')

    # 获取大盘及情绪数据
    # get_train_data('2014-12-01', '2016-05-01', 'VIP_day.csv')
    # get_train_data_hour('2016-07-01', '2016-08-02', '20141201-20160501_hour_mood.csv')
    # get_train_data_from_csv('data/20141201-20150916.csv', 'data/20141201-20150916_比值_分类.txt')

    # 获取关键词数据
    # get_train_stock_keyword('data/2015年大盘_开收盘数据.csv', 'data/0804_trade_time.txt')

    # 测评预测结果
    # get_prediction_real_data('2014-11-31', '2016-05-01', '2014-12-01_2016-04-30_prediction.csv')

    # 2014-12-01 ~ 2015-05-01
    # get_train_from_history('cla_lag10.csv')
