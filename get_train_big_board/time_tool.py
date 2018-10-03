#coding:utf-8
__author__ = 'Kay'

from dateutil import parser
import datetime
import time


# 得到当前时间的上前两个小时
def get_now_last_hour(rule):
    now = get_now(rule)
    dt = datetime.datetime.strptime(now, rule)
    time_delta = datetime.timedelta(hours=1)
    dt1 = dt - time_delta
    dt2 = dt1 - time_delta
    return dt1.strftime(rule), dt2.strftime(rule)


def get_now_last_day(rule):
    now = get_now(rule)
    dt = datetime.datetime.strptime(now, rule)
    time_delta = datetime.timedelta(days=1)
    dt1 = dt - time_delta
    return dt1.strftime(rule)


def get_last_2_hour(dt, rule):
    dt1 = datetime.datetime.strptime(dt, rule)
    time_delta = datetime.timedelta(hours=2)
    dt2 = dt1 - time_delta
    return dt2.strftime(rule)     


def get_now(rule):
    return time.strftime(rule, time.localtime(time.time()))


def add_day(str_datetime):
    '''
    :param str_datetime: 时间字符串
    :return: +1day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, "%Y%m%d%H")
    time_delta = datetime.timedelta(days=1)
    dt = dt + time_delta
    # print dt
    return dt.strftime("%Y%m%d%H")


def add_day_rule(str_datetime, rule):
    '''
    :param str_datetime: 时间字符串
    :return: +1day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, rule)
    time_delta = datetime.timedelta(days=1)
    dt = dt + time_delta
    # print dt
    return dt.strftime(rule)


def add_hour_rule(str_datetime, rule):
    '''
    :param str_datetime: 时间字符串
    :return: +1day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, rule)
    time_delta = datetime.timedelta(hours=1)
    dt = dt + time_delta
    # print dt
    return dt.strftime(rule)


def add_hour(str_datetime):
    '''
    :param str_datetime: 时间字符串
    :return: +1day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, "%Y%m%d%H%M")
    time_delta = datetime.timedelta(hours=1)
    dt = dt + time_delta
    # print dt
    return dt.strftime("%Y%m%d%H%M")

def make_list_days(start, count_days):
    list_days = []
    while count_days > 0:
        list_days.append(start)
        start = plus_day(start)
        count_days -= 1
    return list_days


# print make_list_days("2014120100", 63)
# print "2014"[:-2]
# str_dt = '2014021901'
# print plus_day(str_dt)
# 1417363200 1417363500
# print (long(make_timestamp('2014-12-01 00:06')[:-2]) - 1417363200) / 300

if __name__ == '__main__':
    dt = '201503010000'
