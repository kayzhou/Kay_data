# -*- coding: utf-8 -*-
__author__ = 'Kay Zhou'


'''
获取微博用户的id及昵称
'''

import db_hbase
import db_mysql
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


def add_month(s):
    month = int(s[-2:])
    year = int(s[:-2])
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return str(year) + str(month).zfill(2)


def sub_month(s):
    month = int(s[-2:])
    year = int(s[:-2])
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    return str(year) + str(month).zfill(2)


def get_weibo_user_month(list_id, date):
    rst = db_hbase.scan_tweet_uid_name(list_id, 'search_keytweets' + date[:-2], date)
    with open('data/uid_name/%s_uid_name.txt' % date, 'w') as f:
        for k, v in rst.items():
            f.write(k + '\t' + v + '\n')


if __name__ == '__main__':
    list_id = db_mysql.get_keyword_id()

    # 每月2日启动该任务
    now = arrow.now().format("YYYYMM")
    start = sub_month(now) + '01'
    end = now + '01'
    print(start, end)


    dt = start
    # dt = '20170225'
    while dt < end:
         print(dt)
         get_weibo_user_month(list_id, dt)
         dt = add_day(dt)
