#---------------------------------------------------
# File Name: visual.py
# Author: Kay Zhou
# mail: kayzhou.mail@gmail.com
# Created Time: 2016-07-19 23:08
#---------------------------------------------------
#coding:utf-8

import json

for line in open('data/weibo_20160719/2082306984'):
    dat = json.loads(line)
    for k, v in dat.items():
        if k in set(['id', 'created_at', 'text', 'source', 'reposts_count', 'comments_count', 'attitudes_count']):
            print(k, '>>>', v)
    print('-------------- weibo end --------------')


