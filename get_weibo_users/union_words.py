__author__ = 'Kay Zhou'

import os
import datetime
import arrow


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
                word, count = line.strip().split('\t')
                uid_name[word] = int(count)
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

    out_dict = sorted(uid_name.items(), key=lambda d:d[1], reverse = True)
    with open('/data2/union_words/%s-%s.txt' % (year, str(month).zfill(2)), 'w') as f:

        for k, v in out_dict:
            f.write(k + '\t' + str(v) + '\n')


def union_users_stock(month, in_dir='data/uid_name'):

    def get_weibo_user_from_file(in_name):
        print(in_name)
        for line in open(in_name):
            try:
                uid, name, count = line.strip().split('\t')
                if uid in uid_name:
                    history = uid_name[uid][1]
                    uid_name[uid] = [name, history + int(count)]
                else:
                    uid_name[uid] = [name, int(count)]
            except:
                print('error line ->', line)

    uid_name = {}
    today = '2016' + str(month).zfill(2) + '01'
    if month == 12:
        end = '20170101'
    else:
        end = '2016' + str(month + 1).zfill(2) + '01'

    while today < end:
        get_weibo_user_from_file(in_dir + '/' + today + '_stock.txt')
        today = add_day(today)

    with open('/data2/stock_uid_name/2016-%s.txt' % str(month).zfill(2), 'w') as f:
        for k, v in uid_name.items():
            f.write(k + '\t' + v[0] + '\t' + str(v[1]) + '\n')


def union_all(in_dir='/data2/union_words'):

    def get_weibo_user_from_file(in_name):
        print(in_name)
        for line in open(in_name):
            try:
                word, count = line.strip().split('\t')
                uid_name[word] = int(count)
            except:
                print('error line ->', line)

    uid_name = {}

    for in_name in os.listdir(in_dir):
        get_weibo_user_from_file(in_dir + '/' + in_name)

    out_dict = sorted(uid_name.items(), key=lambda d:d[1], reverse = True)
    with open('2017-01~2017-04.txt', 'w') as f:

        for k, v in out_dict:
            f.write(k + '\t' + str(v) + '\n')


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
    #for i in range(1, 5):
    #    union_users('2017', i)

    #for i in range(10, 13):
    #    union_users_stock(i)

    union_all()
    # exit(-1)

