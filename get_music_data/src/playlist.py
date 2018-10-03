# -*- coding: utf-8 -*-
"""
@author: kayzhou
"""

import json
import multiprocessing
import os

import cloudmusic_new
import send_email


def insert_playlist(pid):
    data = cloudmusic_new.get_playlist(pid)
    json.dump(data, open('../data/playlist/{}.json'.format(pid), 'w'), indent=4, ensure_ascii=False)


def task(pids):
    for pid in pids:
        insert_playlist(pid)


def main():
    print('获取pid完成！')
    pids = set([line.strip() for line in open('pids-20170601.txt').readlines()])
    have_pids = set([os.path.splitext(f_name)[1] for f_name in os.listdir('../data/playlist/')])
    pids = list(pids - have_pids)

    # 歌单较少不需要用多线程
    if len(pids) < 10:
        task(pids)
        return 0

    task_cnt = 5
    step = int(len(pids) / 5)
    for i in range(task_cnt):
        if i == task_cnt-1:
            slice_pids = pids[i * step:]
        else:
            slice_pids = pids[i * step: (i + 1) * step]
        t = multiprocessing.Process(target=task, args=(slice_pids,))
        t.start()


if __name__=='__main__':
    try:
        main()
    except Exception as e:
        send_email.alert('获取歌单详情：' + str(e))
