# -*- coding: utf-8 -*-
__author__ = 'Kay'

import os
import json

data = {}
dir_name = 'data/stock20141201-20161017'

for in_name in os.listdir(dir_name):
    if in_name not in ['股市.txt', '股票.txt', '上证指数.txt', '成分指数.txt', '深成指.txt', '证券.txt']:
        continue
    print(in_name, '分析中...')

    with open(os.path.join(dir_name, in_name)) as f:
        for line in f.readlines():
            w = json.loads(line.strip())
            uid = w['w:uid']
            if uid in data:
                data[uid]['weibo_count'] += 1
                if data[uid]['followers_count'] < int(w['w:followers_count']):
                    data[uid]['followers_count'] = int(w['w:followers_count'])
            else:
                data[uid] = {
                    'name': w['w:screen_name'],
                    'weibo_count': 1,
                    'followers_count': int(w['w:followers_count'])
                }


out_file = open('dapan20141201-20161017_users.txt', 'w')
for k, v in data.items():
    out_file.write(','.join([k, v['name'], str(v['weibo_count']), str(v['followers_count'])]) + '\n')
