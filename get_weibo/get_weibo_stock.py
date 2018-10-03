# coding:utf-8
__author__ = 'Kay'

import json
import datetime
import db_mysql
import db_hbase
import time
import sys

dapan_id_set = (84, 85, 469, 482, 483, 10369)


def datetime_to_stamp(t):
    return time.mktime(t.timetuple())


def get_weibo(keyword, start_time, end_time):
    rst = db_mysql.select_keyword(keyword)
    if len(rst) == 0:
        return {}
    keyword_id = -1
    for row in rst:
        keyword_id = row[0]
    if keyword_id == -1:
        return {'error':'keyword not exists'}
    start_stamp = datetime_to_stamp(start_time)
    end_stamp = datetime_to_stamp(end_time)
    start = str(keyword_id).zfill(5) + str(int(start_stamp))
    end = str(keyword_id).zfill(5) + str(int(end_stamp))

    # 8月11日作为换表分割点
    if keyword_id in dapan_id_set and start_time > datetime.datetime(2015, 8, 11):
        table_name = 'real_search_keytweets'
    else:
        table_name = 'search_keytweets%s%s' % (start_time.year, str(start_time.month).zfill(2))

    tweet_list = db_hbase.scan_tweet(table_name, start, end)
    return tweet_list


def plus_day(dt):
    return dt + datetime.timedelta(days=1)


def get_stock_keyword(in_name):
    keywords = []
    for line in open(in_name):
        w = line.strip().split(',')
        keywords.append(w[0])
        keywords.append(w[1].lower().replace(' ', ''))
    return keywords


def list_to_str(list_data):
    tmp_str = ''
    for str_data in list_data:
        tmp_str = tmp_str + str(str_data) + '\n'
    return tmp_str


def get_weibo_main():
    keywords = get_stock_keyword('word_list/stock_related.txt')
    for word in keywords:
        start_time = datetime.datetime.strptime('2014120100', '%Y%m%d%H')
        end = datetime.datetime.strptime('2016101800', '%Y%m%d%H')
        out_file = open('data/stock20141201-20161017/' + word + '.txt', 'w')

        while start_time < end:
            print(start_time)
            tweet_list = get_weibo(word, start_time, plus_day(start_time))
            for tweet in tweet_list:
                out_file.write(json.dumps(tweet) + '\n')

            start_time = plus_day(start_time)


if __name__ == '__main__':
    get_weibo_main()
