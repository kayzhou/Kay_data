#coding:utf-8

import codecs
import os
import urllib2, urllib
import json
import traceback
import math
import datetime

url = 'http://192.168.1.130/queryUserWeibo?'


def str2datetime(s):
    '''
    Example: Sat Jun 12 23:40:00 +0800 2010 -> datetime.datetime(2010, 6, 12, 23, 40)
    :param s:
    :return:
    '''
    return datetime.datetime.strptime(s[:-11] + s[-5:], '%c')


def crawl(uid, out_file):

    while True:
        params = urllib.urlencode({'uid': uid, 'count': 1, 'page': 1})
        rst = urllib2.urlopen(url + params).read()
        rst = json.loads(rst)
        # print rst

        if 'errno' in rst:
            # 网络错误
            if rst['errno'] == -100:
                print 'Continue!'
                continue
            # 其它错误直接返回
            else:
                print 'Error!'
                break

        def b2i(bo):
            '''
            boolean类型转成可识别的int
            :param bo:
            :return:
            '''
            return str(int(bo))


        raw_data = rst['statuses'][0]['user']
        x = []
        x.append(raw_data['id'])
        if raw_data['gender'] == 'm':
            x.append('1')
        else:
            x.append('0')
        # 注册到2016年3月18日的天数
        res = (datetime.datetime(2016, 3, 2)-str2datetime(raw_data['created_at'])).days
        x.append(math.log(res))
        x.append(math.log(float(raw_data['statuses_count'])))
        x.append(float(raw_data['statuses_count']) / res)
        x.append(math.log(float(raw_data['friends_count']) + 1))
        x.append(math.log(float(raw_data['followers_count']) + 1))
        x.append(float(raw_data['statuses_count']) / (float(raw_data['friends_count']) + 1))
        x.append(float(raw_data['followers_count']) / (float(raw_data['friends_count']) + 1))

        x.append(b2i(raw_data['verified']))
        x.append(b2i(raw_data['allow_all_comment']))
        x.append(b2i(raw_data['allow_all_act_msg']))
        x.append(b2i(raw_data['geo_enabled']))

        x.append(len(raw_data['description']))

        out_file.write(' '.join([str(x) for x in x]) + '\n')
        break


f = file('uid.txt')
uid_list = []
for line in f:
    uid = line.strip()
    uid_list.append(int(uid))
f.close()

out_file = file('users_20160318.txt', 'a')
for uid in uid_list:
    print uid
    try:
        crawl(uid, out_file)
    except:
        print '---------- except! ----------'
