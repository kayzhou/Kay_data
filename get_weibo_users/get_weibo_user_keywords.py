# -*- coding: utf-8 -*-
__author__ = 'Kay Zhou'


'''
获取2015年-2016年微博用户的id及昵称

关键词：股市
'''

import db_hbase
from db_mysql import get_keyword_id
import datetime


def add_day(str_datetime, n=1, rule='%Y%m%d'):
    '''
    :param str_datetime: 时间字符串
    :return: +n day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, rule)
    time_delta = datetime.timedelta(days=n)
    dt = dt + time_delta
    return dt.strftime(rule)


def get_weibo_user(keyword_id, date):
    '''
    根据关键词id和日期获取用户信息
    :param keyword_id:
    :param date:
    :return:
    '''
    rst = db_hbase.scan_tweet_user_keyword(keyword_id, date)
    with open('data/uid_name/保险/%s.txt' % date, 'w') as f:
        for k, v in rst.items():
            f.write(k + ',' + ','.join([str(value) for value in v]) + '\n')


if __name__ == '__main__':
    keyword_id = get_keyword_id('保险')
    today = '20140901'
    while today < '20170101':
        get_weibo_user(keyword_id, today)
        today = add_day(today)
