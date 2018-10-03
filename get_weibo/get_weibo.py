#coding:utf-8
__author__ = 'Kay'

import json
import datetime
import sys
import db_mysql
import db_hbase
import time


dapan_id_set = set([84, 85, 469, 482, 483, 10369])


def datetime_to_stamp(t):
    return time.mktime(t.timetuple())


def get_weibo(keyword,start_time,end_time):
    rst=db_mysql.select_keyword(keyword)
    if len(rst)==0:
        return {}
    keyword_id=-1
    for row in rst:
        keyword_id=row[0]
    if keyword_id==-1:
        return {}
    start_stamp=datetime_to_stamp(start_time)
    end_stamp=datetime_to_stamp(end_time)
    start=str(keyword_id).zfill(5)+str(int(start_stamp))
    end=str(keyword_id).zfill(5)+str(int(end_stamp))

    # 8月11日作为换表分割点
    if keyword_id in dapan_id_set and start_time > datetime.datetime(2015, 8, 11):
        table_name = 'real_search_keytweets'
    else:
        table_name='search_keytweets%s%s' % (start_time.year,str(start_time.month).zfill(2))

    tweet_list=db_hbase.scan_tweet(table_name,start,end)
    return tweet_list


def plus_day(dt):
    return dt + datetime.timedelta(days=1)


def get_keyword(filename):
    keywords = list()
    fi = open(filename)
    for line in fi.readlines():
        keywords.append(line.strip().split('\t')[0])
    return keywords


def list_to_str(list_data):
    tmp_str = ''
    for str_data in list_data:
        tmp_str = tmp_str + str(str_data) + '\n'
    return tmp_str


def get_weibo_main():
    # keywords = get_keyword('dapan_word_list.txt')
    # keywords = ['郭广昌', '王健林', '马云', '复星', '万达', '阿里']
    keywords = ['马化腾', '腾讯', '华为', '任正非']
    for word in keywords:
        start_time = datetime.datetime.strptime('2017010100', '%Y%m%d%H')
        end = datetime.datetime.strptime('2017032000', '%Y%m%d%H')
        out_file = open('data/' + word + '.txt', 'w')

        all_tweet = []
        while start_time < end:
            print word, start_time

            # tweet_list = get_weibo(word, start_time, plus_day(start_time))
            # for tweet in tweet_list:
            #     写到文件，这行就够了！
            #     out_file.write(json.dumps(tweet) + '\n')
            #
            #     print '>>>'
            #     for k, v in tweet.iteritems():
            #         print k[2:]+':', v

            all_tweet += get_weibo(word, start_time, plus_day(start_time))
            start_time = plus_day(start_time)

        # json.dump(all_tweet, out_file, indent=4)
        for t in all_tweet:
            out_file.write(json.dumps(t) + '\n')


if __name__ == '__main__':
    get_weibo_main()
