#coding:utf-8
import happybase
import multiprocessing
import db_mysql
import json
import traceback
import sys

'''
由Hbase中获取用户微博数据
'''

def user_tweets(conn, id, table_name1, table_name2, fout):
    table = conn.table(table_name1)
    # table_weibo = conn.table(table_name2)

    for key, data in table.scan(row_prefix = id):
        try:
            weibo = json.loads(data['w:'])
            fout.write(json.dumps(weibo)+'\n')
        except:
            traceback.print_exc(file = sys.stderr)


def task(host, uid_list):
    conn = happybase.Connection(host)
    for uid in uid_list:

        print 'uid:', uid
        out_file = open('data/user_music_hbase/%s' % uid, 'w')
        id = db_mysql.find(uid)
        if id == -1:
            print 'no this uid.'
            continue
        else:
            id = str(id).zfill(10)
        user_tweets(conn, id, 'userstamp_weibo2014', 'user_tweets2014', out_file)
        user_tweets(conn, id, 'userstamp_weibo2015', 'user_tweets2015', out_file)
        user_tweets(conn, id, 'userstamp_weibo2016', 'user_tweets2016', out_file)
        out_file.close()


if __name__ == '__main__':
    host_list = []
    for i in range(3, 8):
        host_list.append('beihang%s' % i)

    uid_list = [line.strip() for line in open('uid/weibo_id_music.txt')]

    # 用户较少不需要用多线程
    if len(uid_list) < 10:
        task(host_list[0], uid_list)
        exit()

    task_cnt = 5
    step = len(uid_list) / 5
    for i in range(task_cnt):
        host = host_list[i]
        if i==task_cnt-1:
            slice_uid_list = uid_list[i*step:]
        else:
            slice_uid_list = uid_list[i*step:(i+1)*step]
        t = multiprocessing.Process(target = task, args=(host, slice_uid_list))
        t.start()
