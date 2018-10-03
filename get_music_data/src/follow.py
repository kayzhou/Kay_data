# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 12:24:07 2017

@author: HAPPENQ
"""

import datetime
import json
import re
import time
import random
import cloudmusic_new
import send_email
import arrow

import pymongo as pm
from selenium import webdriver
driver = webdriver.PhantomJS(executable_path=
                             '../phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
                             # '../phantomjs-2.1.1-macosx/bin/phantomjs')

client=pm.MongoClient('192.168.1.109', 27017)
db=client.music


def get_user_history(uid):
    '''
    :param uid:
    :return:
    '''
    url='http://music.163.com/#/user/songs/rank?id={0}'.format(uid)
    print(uid)
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        return []
    driver.switch_to.frame('contentFrame')
    #num_all_songs='0'
    #try:
    #    num_all_songs=driver.find_element_by_xpath('//*[@id="rHeader"]/h4').text
    #except:
    #    num_all_songs='0'
    #print num_all_songs
    #numOfsongs=int(re.findall(r"\d+",num_all_songs)[0])
    songs_all_id=[]
    #print "所有时间"
    try:
        driver.find_element_by_xpath('//*[@id="songsall"]').click()
    except Exception as e:
        print(e)
        return []
    # time.sleep(4)

    # 遍历100首歌
    for j in range(1, 101):
        try:
            print(j)
            song_item={}
            song_item['song_id']=driver.find_element_by_xpath(
                '//*[@id="m-record"]/div/div[1]/ul/li[{0}]/div[2]/div[1]/div/span/a'.format(str(j))).get_attribute('href').split('=')[1]

            song_item['song_name']=driver.find_element_by_xpath(
                '//*[@id="m-record"]/div/div[1]/ul/li[{0}]/div[2]/div[1]/div/span/a/b'.format(str(j))).text


            song_item['artist']=driver.find_element_by_xpath(
                '//*[@id="m-record"]/div/div[1]/ul/li[{0}]/div[2]/div[1]/div/span/span/span/a'.format(str(j))).text

            proper=driver.find_element_by_xpath(
                '//*[@id="m-record"]/div/div[1]/ul/li[{0}]/div[3]/span'.format(str(j))).get_attribute('style')
            song_item['score']=int(re.findall(r"\d+", proper)[0])

        except Exception as e:
            print(e)
            break
        else:
            songs_all_id.append(song_item)
    #print len(songs_all_id)
    #driver.quit()
    #print numOfsongs,songs_week_id,songs_all_id
    return songs_all_id


def get_weibo_users(in_name):
    user_ids = [line.strip().split(',') for line in open(in_name)]
    return user_ids


def save_to_db_history(user_info_list,user_all_tk):
    collection=db.history
    insert_list={}
    insert_list['_id']=user_info_list[0]
    insert_list['wid']=user_info_list[1]
    insert_list['uid']=user_info_list[0]
    insert_list['trackCount'] = len(user_all_tk)
    insert_list['collUpdateTime'] = int(round(time.time() * 1000))
    insert_list['tracks'] = user_all_tk
    collection.insert(insert_list)


def insert_data():
    weibo_list = get_weibo_users('../data/uid_wid_1000.txt')
    for i, line in enumerate(weibo_list):
        if i < 36079:
            continue
        uid = line[0]
        print(i, '->', uid)
        data = cloudmusic_new.get_user_follows(uid)
        # time.sleep(random.randint(100, 2000) / 1000)
        json.dump(data, open('../data/follow/{}.txt'.format(uid), 'w'), indent=4, ensure_ascii=False)
        '''
        songs_all=get_user_history(uid)
        time.sleep(random.randint(1, 5))
        if len(songs_all)!=0:
            save_to_db_history(line, songs_all)
            # print 'history:',line[0],'is saved'
        else:
            print(line[0], 'history is none')
        '''


if __name__=='__main__':
    try:
        insert_data()
    except Exception as e:
        send_email.alert('历史听歌记录：' + str(e))
