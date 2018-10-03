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


def union_users(year, month, in_dir='data/uid_name/保险'):

    def get_weibo_user_from_file(in_name):
        print(in_name)
        for line in open(in_name):
            try:
                info = line.strip().split(',')
                uid = info[0]
                if uid not in uid_name:
                    uid_name[uid] = info[1:]
                else:
                    # 原有微博数
                    weibo_count = int(uid_name[uid][-1])
                    info[-1] = str(int(info[-1]) + weibo_count)
                    uid_name[uid] = info[1:]
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
        get_weibo_user_from_file(in_dir + '/' + today + '.txt')
        today = add_day(today)

    with open('/data2/uid_name/保险/%s-%s.txt' % (year, str(month).zfill(2)), 'w') as f:
        for k, v in uid_name.items():
            # print(v)
            if k != '':
                f.write(k + ',' + ','.join(v) + '\n')


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


def union_all(in_dir='/data2/uid_name'):
    uids = set()
    for in_name in os.listdir(in_dir):
        if (not in_name.startswith('20')) or len(in_name) != 11:
            continue
        print(in_name)
        for line in open(os.path.join(in_dir, in_name)):
            uids.add(line.strip().split('\t')[0])
    print(len(uids))


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
    year = '2016'
    for month in range(1, 13):
        union_users(year, month)

    #for i in range(10, 13):
    #    union_users_stock(i)

    # union_all()
    # exit(-1)

    # 合并上月的用户数据
    #now = arrow.now().format("YYYYMM")
    #now = sub_month(now)
    #union_users(now[:4], int(now[-2:]))

