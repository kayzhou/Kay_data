# -*- coding: utf-8 -*-
__author__ = 'Kay'

import os
import sys
import json
import pymongo
import arrow
import time
import random
from music_handler import *
from mongo_handler import get_playlist_coll
from mongo_handler import get_mongo_pids
import cloudmusic_new


# def crawl():
#     '''
#     爬取网易云音乐用户基本信息及其歌单
#     :return:
#     '''
#     had_been_crawled, seed_user = init()
#     uid_weiboUid = [seed_user]
#
#     out_file = open('data/uid_weiboUid.txt', 'a')
#
#     while len(uid_weiboUid) > 0:
#
#         uid = uid_weiboUid[0]['uid']
#
#         print '-' * 40
#         print '目前待爬用户数', len(uid_weiboUid)
#         print '累积用户数', len(had_been_crawled)
#         print '用户', uid, uid_weiboUid[0]['name']
#
#         next_uids = get_followers_by_id(uid) + get_friends_by_id(uid)
#         for next_uid in next_uids:
#
#             # 判断是否放在或放过待爬列表
#             if next_uid in had_been_crawled:
#                 continue
#             else:
#                 had_been_crawled.add(next_uid)
#
#             # 新的用户来了
#             user = get_user_by_id(next_uid)
#             out_file.write(json.dumps(user, ensure_ascii=False) + '\n')
#             uid_weiboUid.append(user)
#
#             # 保存TA的歌单
#             print '获取 {0} 歌单中 ...'.format(user['uid'])
#             if not os.path.exists('data/user_playlists/{0}.json'.format(user['uid'])):
#                 json.dump(get_playlists_by_id(user['uid']),
#                           open('data/user_playlists/{0}.json'.format(user['uid']), 'w'),
#                           ensure_ascii=False, indent=4)
#
#         # 当前查询的用户从列表中删除
#         del uid_weiboUid[0]
#         out_file.flush()


def crawl_user_playlist(in_name='../data/uid_weiboUid.txt'):
    bingo = False
    for line in open(in_name):
        d = json.loads(line.strip())
        uid = d['uid']
        if uid == '115006802':
            bingo = True
        if not bingo:
            continue
        print('获取 {0} 歌单中 ...'.format(uid))
        if not os.path.exists('../data/user_playlists/{}.json'.format(uid)):
            json.dump(get_playlists_by_id(uid), open(
                '../data/user_playlists/{}.json'.format(uid), 'w'), indent=4, ensure_ascii=False)


def insert_playlist(pid, coll):
    '''
    歌单信息放入MongoDB
    '''
    # p_list = json.load(open(in_name))["playlist"]

    # 记录pid
    # have_pids.add(pid)
    # continue

    # 获取歌单详细信息
    print(arrow.now().format(), '->', pid)
    data = get_playlist_by_pid(pid)
    print(data)
    # data = cloudmusic_new.get_playlist(pid)
    time.sleep(random.randint(1, 5))

    # 存储至文件
    json.dump(data, open('/data2/cloudmusic/playlists/{}.json'.format(pid), 'w'), indent=4, ensure_ascii=False)
    data['_id'] = pid

    # 存储至MongoDB
    try:
        coll.insert(data)
    except pymongo.errors.DuplicateKeyError:
        print('Duplicate Kay Error.')


if __name__ == '__main__':


    # crawl()
    # crawl_user_playlist()


    '''
    获取歌单详情，存储至文件和MongoDB
    '''
    # in_dir = '/data2/cloudmusic/user_playlists'
    # have_pids = get_mongo_pids()
    # print('获取pid完成！')
    # playlist_coll = get_playlist_coll()
    # for in_file in os.listdir(in_dir):
    #     print(in_file)
    #     insert_playlist(in_dir + '/' + in_file, playlist_coll, have_pids)
        # print('len(pids) ->', len(have_pids))

    # pid_txt = open('pid.txt', 'w')
    # for p in have_pids:
    #     pid_txt.write(str(p) + '\n')

    pids = [line.strip() for line in open('pids.txt').readlines()]
    print(len(pids))
    # have_pids = get_mongo_pids()
    have_pids = set([line.strip() for line in open('have_pids.txt').readlines()])
    print(len(have_pids))
    print('获取pid完成！')

    playlist_coll = get_playlist_coll()

    for pid in pids:
        if pid in have_pids:
            continue
        try:
            insert_playlist(pid, playlist_coll)
            have_pids.add(pid)
        except Exception as e:
            print('Exception:', pid, e)

        print('len(pids) ->', len(have_pids))
