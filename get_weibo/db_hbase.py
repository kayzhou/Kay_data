#coding:utf-8
import traceback,sys
import random
import happybase


def get_hbase_con():
    host_list=['beihang1','beihang2','beihang3','beihang4','beihang5','beihang6','beihang7']
    while True:
        try:
            host=host_list[random.randint(0,6)]
            con=happybase.Connection(host)
            return con
        except:
            traceback.print_exc(file=sys.stderr)


def scan_tweet(table_name, start, stop):
    con=get_hbase_con()
    table=con.table(table_name)
    rst=table.scan(row_start=start, row_stop=stop)
    tweet_list=[]
    for key,data in rst:
        weiboid = key[15:]
        data['id'] = weiboid
        tweet_list.append(data)
    return tweet_list


def scan_tweet_uid_name(table_name):
    con=get_hbase_con()
    table=con.table(table_name)
    print('Table ->', table_name)
    rst=table.scan(row_start='0' * 31, row_stop='9' * 31, columns=['w:uid', 'w:screen_name'])
    dict_uid_name = {}
    count = 0
    for key, data in rst:
        count += 1
        if count % 100000 == 0:
            print(count)
            dict_uid_name[data['w:uid']] = data['w:screen_name']
    return dict_uid_name
