__author__ = 'Kay Zhou'

import os
import datetime
import arrow
import traceback, sys


def add_day(str_datetime, n=1, rule='%Y%m%d'):
    '''
    :param str_datetime: 时间字符串
    :return: +n day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, rule)
    time_delta = datetime.timedelta(days=n)
    dt = dt + time_delta
    return dt.strftime(rule)


def union_users(year, month, in_dir='data/uid_name'):

    def get_weibo_user_from_file(in_name):
        print(in_name)
        for line in open(in_name):
            try:
                uid, name = line.strip().split('\t')
                uid_name[uid] = name
            except:
                print('error line ->', line)

    print(year, month, 'merging!')
    uid_name = {}
    today = year + str(month).zfill(2) + '01'
    if month == 12:
        end = str(int(year) + 1) + '0101'
    else:
        end = year + str(month + 1).zfill(2) + '01'

    while today < end:
        get_weibo_user_from_file(in_dir + '/' + today + '_uid_name.txt')
        today = add_day(today)

    with open('/data2/uid_name/%s-%s.txt' % (year, str(month).zfill(2)), 'w') as f:
        for k, v in uid_name.items():
            f.write(k + '\t' + v + '\n')


def union_users_stock(year, month, in_dir='data/uid_name/股市'):
    '''
    合并股市用户
    :param year:
    :param month:
    :param in_dir:
    :return:
    '''
    def get_weibo_user_from_file(in_name):
        print(in_name)
        for line in open(in_name):
            try:
                words = line.strip().split(',')
                uid = words[0]
                others = words[1:-1]
                weibo_count = int(words[-1])
                if uid in dict_user_data:
                    original_count = dict_user_data[uid][-1]
                    dict_user_data[uid][-1] = original_count + weibo_count
                else:
                    user_data = [uid]
                    user_data.extend(others)
                    user_data.append(weibo_count)
                    dict_user_data[uid] = user_data
            except:
                print('error line ->', line)

    dict_user_data = {}

    # 起止时间
    today = year + str(month).zfill(2) + '01'
    if month == 12:
        end = str(int(year) + 1) + '0101'
    else:
        end = year + str(month + 1).zfill(2) + '01'

    # 遍历时间
    while today < end:
        get_weibo_user_from_file(in_dir + '/' + today + '.txt')
        today = add_day(today)


    with open('/data2/stock_uid_name/{}-{}.txt'.format(year, str(month).zfill(2)), 'w') as f:
        for v in dict_user_data.values():
            f.write(','.join([str(value) for value in v]) + '\n')


def union_users_stock_all(file_list):
    '''
    合并全部股市用户
    :param year:
    :param month:
    :param in_dir:
    :return:
    '''
    def get_weibo_user_from_file(in_name):
        print(in_name)
        for line in open(in_name):
            try:
                words = line.strip().split(',')
                uid = words[0]
                others = words[1:-1]
                weibo_count = int(words[-1])
                if uid in dict_user_data:
                    original_count = dict_user_data[uid][-1]
                    dict_user_data[uid][-1] = original_count + weibo_count
                else:
                    user_data = [uid]
                    user_data.extend(others)
                    user_data.append(weibo_count)
                    dict_user_data[uid] = user_data
            except:
                print('error line ->', line)

    dict_user_data = {}

    # 遍历文件
    for in_name in file_list:
        get_weibo_user_from_file(in_name)

    dict_user_data = sorted(dict_user_data.items(), key=lambda d: d[1][-1], reverse=True)
    with open('/data2/stock_uid_name/201601-201703.txt', 'w') as f:
        f.write('用户ID,昵称,微博数,关注数,粉丝数,相互关注数,性别,位置,用户创建时间,关键词微博数\n')
        for k, v in dict_user_data:
            f.write(','.join([str(value) for value in v]) + '\n')


def sub_month(s):
    month = int(s[-2:])
    year = int(s[:-2])
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    return str(year) + str(month).zfill(2)


if __name__ == '__main__':
    #for i in range(9, 13):
    #    union_users('2014', i)

    # year = '2016'
    # for i in range(9, 13):
    #    union_users_stock(year, i)

    year = '2017'
    try:
        for i in range(1, 4):
            union_users_stock(year, i)
    except:
        traceback.print_exc(file=sys.stderr)

    in_dir = '/data2/stock_uid_name/'
    in_names = ['2017-01.txt', '2017-02.txt', '2017-03.txt']
    in_names = [in_dir + name for name in in_names]
    union_users_stock_all(in_names)

