import codecs
import os
__author__ = 'kayzhou'
import json
import traceback, sys
import time
import requests
import multiprocessing


url = 'http://192.168.1.130/queryUserWeibo?'

def crawl(uid):

    in_name = 'data/user_music/%s' % uid
    if os.path.exists(in_name) and os.path.getsize(in_name) > 0:
        print 'File exists!'
        return -1


    fout = open('data/user_music/%s' % uid, 'w')
    page = 0
    retry = 0
    while page < 10 and retry < 5:
        print 'PAGE:', page
        sys.stdout.flush()

        try:
            para= {'uid': uid, 'count': 100, 'page': page + 1}
            rst = requests.get(url, params=para).json()

            if 'errno' in rst:
                if rst['errno'] == -100:
                    print 'error is -100, continue!'
                    retry += 1
                    continue

            if not 'statuses' in rst:
                print 'KeyError: contunue!'
                retry += 1
                continue

            tweet_list = rst['statuses']

            if not tweet_list:
                'Tweet is null.'
                break

            print 'Length of tweets is %s' % len(tweet_list)
            for tweet in tweet_list:
                fout.write(json.dumps(tweet) + '\n')
            time.sleep(0.1)
            page += 1
            retry = 0

        except:
            print rst
            page += 1
            traceback.print_exc(file=sys.stderr)
    fout.close()


def task(what, uid_list):
    for uid in uid_list:
        print 'uid:', uid
        crawl(uid)


if __name__ == '__main__':
    uid_list = [line.strip() for line in open('uid/weibo_id_music.txt')]

    if len(uid_list) < 10:
        task(uid_list)
        exit()

    task_cnt = 20
    step = len(uid_list) / task_cnt

    for i in range(task_cnt):
        if i==task_cnt-1:
            slice_uid_list = uid_list[i * step:]
        else:
            slice_uid_list = uid_list[i * step: (i+1) * step]
        t = multiprocessing.Process(target = task, args=(1,slice_uid_list))
        t.start()
