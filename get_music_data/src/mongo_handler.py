#coding:utf-8
__author__ = 'Kay'

import pymongo


# 合并两个词典
def union_dict(*objs):
    _keys = set(sum([obj.keys() for obj in objs],[]))
    _total = {}
    for _key in _keys:
        _total[_key] = sum([obj.get(_key,0) for obj in objs])
    return _total


def find(coll, word, dt):
    return coll.find_one({'word':word, 'datetime':dt})


def get_playlist_coll():
    mongo_con = 'mongodb://192.168.1.109:27017'
    return pymongo.MongoClient(mongo_con).music.playlist


def get_song_coll():
    mongo_con = 'mongodb://192.168.1.109:27017'
    return pymongo.MongoClient(mongo_con).music.song_20170602


def get_mongo_pids():
    coll = get_playlist_coll()
    have_pids = []
    skip = 0
    limit = 5000
    while True:
        print('skip ->', skip)
        pids = coll.find({}, {'_id': 1}, skip=skip, limit=limit)
        skip += limit
        count = 0
        for p in pids:
            count += 1
            have_pids.append(str(p['_id']))
        if count == 0:
            break
    out_file = open('have_pids.txt', 'w')
    for p in have_pids:
        out_file.write(p + '\n')

    return have_pids


if __name__ == '__main__':

    # 获取pids
    #print '获取pids ... ...'
    pids = get_mongo_pids()
    count = 0
    with open('data/pids.txt', 'w') as f:
        for i, p in enumerate(pids):
            if not i % 1000:
                print(i)
            f.write(str(p) + '\n')
