# -*- coding: utf-8 -*-
__author__ = 'Kay'


import os
import sys
import time
import json
import traceback
import requests
from mongo_handler import get_song_coll
from mongo_handler import get_playlist_coll
from selenium import webdriver
import pymongo


driver = webdriver.PhantomJS(
    executable_path='../phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    # executable_path='phantomjs-2.1.1-macosx/bin/phantomjs')


def get_user_by_id(uid):
    '''
    获取网易云音乐用户信息
    :param uid:
    :return:
    '''
    url = 'http://music.163.com/#/user/home?id={0}'.format(uid)
    driver.get(url)
    time.sleep(1)
    driver.switch_to_frame('contentFrame')
    name = driver.find_element_by_xpath('//*[@id="head-box"]/dd/div[1]/div/h2/span[1]').text
    event_count = driver.find_element_by_xpath('//*[@id="event_count"]').text
    follow_count = driver.find_element_by_xpath('//*[@id="follow_count"]').text
    fan_count = driver.find_element_by_xpath('//*[@id="fan_count"]').text

    try:
        weiboid = driver.find_element_by_xpath('//*[@id="head-box"]/dd/div[4]/ul/li/a').get_attribute('href').split('/u/')[1]
    except:
        weiboid = '-1'
    try:
        # 若为空则该用户设置隐私
        listen_count = driver.find_element_by_xpath('//*[@id="rHeader"]/h4').text
    except:
        listen_count = '-1'

    user = {
        'uid': uid,
        'wid': weiboid,
        'name': name,
        'event_count': event_count,
        'follow_count': follow_count,
        'fan_count': fan_count,
        'listen_count': listen_count
    }
    return user


def get_followers_by_id(uid):
    '''
    根据用户id，获取粉丝
    '''
    url = 'http://music.163.com/#/user/fans?id={0}'.format(uid)
    driver.get(url)
    time.sleep(1)
    driver.switch_to.frame('contentFrame')
    followers_uids = []
    for i in range(1, 21):
        try:
            re = driver.find_element_by_xpath('//*[@id="main-box"]/li[{0}]/a'.format(str(i)))
            followers_uids.append(re.get_attribute('href').strip().split('id=')[1])
        except:
            break
    return followers_uids


def get_friends_by_id(uid):
    '''
    根据用户id，获取关注对象
    '''
    url = 'http://music.163.com/#/user/follows?id={0}'.format(uid)
    driver.get(url)
    time.sleep(1)
    driver.switch_to_frame('contentFrame')
    followers_uids = []
    for i in range(1, 21):
        try:
            re = driver.find_element_by_xpath('//*[@id="main-box"]/li[{0}]/a'.format(str(i)))
            followers_uids.append(re.get_attribute('href').strip().split('id=')[1])
        except:
            break
    return followers_uids


def get_playlists_by_id(uid):
    '''
    根据用户id，获取歌单
    '''
    url = 'http://music.163.com/api/user/playlist/?offset=0&limit=100&uid={0}'.format(uid)
    print(url)
    r = requests.get(url)
    return r.json()


def get_playlist_by_pid(pid):
    '''
    根据歌单id，获取详细歌单
    '''
    url = 'http://music.163.com/api/playlist/detail?id={0}'.format(pid)
    try:
        r = requests.get(url)
        print(r.text)
    except:
        traceback.print_exc(file = sys.stderr)
        print(url)
        return -1

    return r.json()


def get_songs_from_mongo_playlists(coll, pid):
    '''
    从beihang9的mongo里面，获取pid歌单的所有歌曲信息, 以及歌单的风格
    '''
    docs = coll.find_one({'_id': pid}, {'_id': 0, 'tracks': 1, 'tags': 1})
    return docs


def get_song_detail_by_sid(sid):
    '''
    根据歌曲id，获取歌曲详细信息
    '''
    url = 'http://music.163.com/api/song/detail/?id={0}&ids=[{0}]'.format(sid)
    return requests.get(url).json()


def init(in_name='data/uid_weiboUid.txt'):
    '''
    获取已经爬到的用户列表, 以及找到一个种子用户
    :param in_name:
    :return:
    '''
    uid_set = set()
    seed_user = {}
    if not os.path.exists(in_name):
        in_name = 'data/init_user.txt'

    for line in open(in_name):
        user = json.loads(line.strip())
        uid = user['uid']
        uid_set.add(uid)
        if int(user['follow_count']) > 20 and user['wid'] != '-1':
            seed_user = user

    return uid_set, seed_user


if __name__ == '__main__':
    # url = 'http://music.163.com/#/user/home?id=88349979'
    # url = 'http://music.163.com/#/user/fans?id=61884303'

    # print get_user_by_id('61884303')
    # print get_user_by_id('116698008')
    # print get_followers_by_id('61884303')
    # print get_friends_by_id('88349979')
    # re = get_playlists_by_id('88349979')
    # re = get_playlist_by_pid('136872551')
    # re = get_song_detail_by_sid('229143')
    # json.dump(re, open('test.txt', 'w'), indent=4)


    # 从歌单数据抽出音乐数据导入MongoDB
    coll = get_playlist_coll()
    m_coll = get_song_coll()
    # 获取所有歌单id
    pids = [int(line.strip()) for line in open('../data/pids.txt').readlines()]
    have_pids = set([int(line.strip()) for line in open('../data/have_pids.txt').readlines()])
    have_song_ids = set([int(line.strip()) for line in open('../data/have_song_ids.txt').readlines()])
    #bingo = False

    for i, pid in enumerate(pids):
        if i < 2537060:
            continue

        if pid not in have_pids:
            continue

        print('row ->', i)

        re = get_songs_from_mongo_playlists(coll, pid)
        if re == None:
            continue
        tracks = re['tracks']
        style = re['tags'] # 歌单风格

        for song in tracks:
            if song['id'] in have_song_ids:
                m_coll.update_one({'_id': song['id']}, {'$inc': {'count_in_playlist': 1}})
                if style:
                    m_coll.update_one({'_id': song['id']}, {"$push": {"style_list": style}})
            else:
                song['_id'] = song['id']
                song['count_in_playlist'] = 1
                if style:
                    song['style_list'] = [style]
                else:
                    song['style_list'] = []
                m_coll.insert(song)
                have_song_ids.add(song['id'])
