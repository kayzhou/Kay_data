# -*- coding: utf-8 -*-
"""
@author: kayzhou
"""

import json
import multiprocessing
import os

import cloudmusic_new
import send_email


def insert_playlist(uid):
    data = cloudmusic_new.get_user_playlist(uid)
    if data['code'] == 200:
        json.dump(data, open('../data/user_playlist/{}.json'.format(uid), 'w'), ensure_ascii=False)


def task(uids):
    for uid in uids:
        insert_playlist(uid)


def main():
    print('获取pid完成！')
    uids = set([line.strip().split(',')[0] for i, line in enumerate(open('../data/uid-wid-count.csv').readlines()) if i > 0])
    have_uids = set([os.path.splitext(f_name)[1] for f_name in os.listdir('../data/user_playlist/')])
    uids = list(uids - have_uids)

    # 歌单较少不需要用多线程
    if len(uids) < 10:
        task(uids)
        return 0

    task_cnt = 5
    step = int(len(uids) / 5)
    for i in range(task_cnt):
        if i == task_cnt-1:
            slice_pids = uids[i * step:]
        else:
            slice_pids = uids[i * step: (i + 1) * step]
        t = multiprocessing.Process(target=task, args=(slice_pids,))
        t.start()


if __name__=='__main__':
    try:
        main()
    except Exception as e:
        send_email.alert('获取用户歌单详情：' + str(e))
