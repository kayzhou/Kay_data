#coding:utf-8
import traceback,sys
import random
import happybase
import time
import datetime


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


def datetime_to_stamp(t):
    return time.mktime(t.timetuple())


def add_day(str_datetime, n=1, rule='%Y%m%d'):
    '''
    :param str_datetime: 时间字符串
    :return: +n day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, rule)
    time_delta = datetime.timedelta(days=n)
    dt = dt + time_delta
    return dt.strftime(rule)


def scan_tweet_uid_name(list_id, table_name, today):
    con=get_hbase_con()
    table=con.table(table_name)
    print('Table ->', table_name, 'Today ->', today)
    dict_uid_name = {}
    start_stamp = datetime_to_stamp(datetime.datetime.strptime(today, '%Y%m%d'))
    end_stamp = datetime_to_stamp(datetime.datetime.strptime(add_day(today), '%Y%m%d'))
    for i, id in enumerate(list_id):
        if not i % 1000:
            print(i, len(dict_uid_name))
        start = str(id).zfill(5) + str(int(start_stamp))
        end = str(id).zfill(5) + str(int(end_stamp))
        try:
            rst = table.scan(row_start=start, row_stop=end, columns=['w:uid', 'w:screen_name'])
            for key, data in rst:
                dict_uid_name[data[b'w:uid'].decode()] = data[b'w:screen_name'].decode()
        except:
            traceback.print_exc(file=sys.stderr)

    return dict_uid_name


def scan_tweet_uid_name_keyword(keyword_id, today):
    con=get_hbase_con()
    dapan_id_set = set([84, 85, 469, 482, 483, 10369])
    if int(keyword_id) in dapan_id_set and today > '20150811':
        table_name = 'real_search_keytweets'
    else:
        table_name = 'search_keytweets%s' % today[:-2]
    table = con.table(table_name)
    print('Table ->', table_name, 'Today ->', today)
    dict_uid_name = {}
    start_stamp = datetime_to_stamp(datetime.datetime.strptime(today, '%Y%m%d'))
    end_stamp = datetime_to_stamp(datetime.datetime.strptime(add_day(today), '%Y%m%d'))
    start = str(keyword_id).zfill(5) + str(int(start_stamp))
    end = str(keyword_id).zfill(5) + str(int(end_stamp))
    try:
        print(start, end)
        rst = table.scan(row_start=start, row_stop=end, columns=['w:uid', 'w:screen_name'])
        for key, data in rst:
            uid = data[b'w:uid'].decode()
            name = data[b'w:screen_name'].decode()
            if uid in dict_uid_name:
                number_of_weibo = dict_uid_name[uid][1]
                dict_uid_name[uid] = [name, number_of_weibo + 1]
            else:
                dict_uid_name[uid] = [name, 1]
    except:
        traceback.print_exc(file=sys.stderr)
    return dict_uid_name


def scan_tweet_user_keyword(keyword_id, today):
    '''
    根据keyword_id和日期（精确到天）
    :param keyword_id:
    :param today:
    :return:
    '''
    con = get_hbase_con()

    dapan_id_set = {84, 85, 469, 482, 483, 10369}

    # 是否是大盘关键词
    if int(keyword_id) in dapan_id_set and today > '20150811':
        table_name = 'real_search_keytweets'
    else:
        table_name = 'search_keytweets%s' % today[:-2]
    table = con.table(table_name)
    print('Table ->', table_name, 'Today ->', today)

    dict_uid_name = {}
    start_stamp = datetime_to_stamp(datetime.datetime.strptime(today, '%Y%m%d'))
    end_stamp = datetime_to_stamp(datetime.datetime.strptime(add_day(today), '%Y%m%d'))
    start = str(keyword_id).zfill(5) + str(int(start_stamp))
    end = str(keyword_id).zfill(5) + str(int(end_stamp))
    try:
        print(start, end)
        rst = table.scan(row_start=start, row_stop=end,
                         columns=['w:uid', 'w:screen_name', 'w:statuses_count',
                                  'w:ucreated_at', 'w:bi_followers_count', 'w:followers_count',
                                  'w:gender', 'w:location', 'w:friends_count'])
        for key, data in rst:
            # 用户id
            uid = data[b'w:uid'].decode()
            # 昵称
            name = data[b'w:screen_name'].decode()
            # 微博数
            statuses_count = data[b'w:statuses_count'].decode()
            # 关注数
            friends_count = data[b'w:friends_count'].decode()
            # 粉丝数
            followers_count = data[b'w:followers_count'].decode()
            # 相互关注数
            bi_followers_count = data[b'w:bi_followers_count'].decode()
            # 性别
            gender = data[b'w:gender'].decode()
            # 位置
            location = data[b'w:location'].decode()
            # 创建时间
            ucreated_at = data[b'w:ucreated_at'].decode()

            # 用户数据
            user_data = [name, statuses_count, friends_count, followers_count,
                    bi_followers_count, gender, location, ucreated_at]

            # 包含该uid
            if uid in dict_uid_name:
                number_of_weibo = dict_uid_name[uid][-1]
                dict_uid_name[uid][-1] = number_of_weibo + 1
            else:
                user_data.append(1)
                dict_uid_name[uid] = user_data

    except:
        traceback.print_exc(file=sys.stderr)
    return dict_uid_name


def scan_word(list_id, table_name, today):
    con=get_hbase_con()
    table=con.table(table_name)
    print('Table ->', table_name, 'Today ->', today)
    word_count = {}
    start_stamp = datetime_to_stamp(datetime.datetime.strptime(today, '%Y%m%d'))
    end_stamp = datetime_to_stamp(datetime.datetime.strptime(add_day(today), '%Y%m%d'))
    for i, id in enumerate(list_id):
        if not i % 1000:
            print(i, len(word_count))
        start = str(id).zfill(5) + str(int(start_stamp))
        end = str(id).zfill(5) + str(int(end_stamp))
        try:
            rst = table.scan(row_start=start, row_stop=end, columns=['w:seg'])
            # print(word_count)
            for key, data in rst:
                words = data[b'w:seg'].decode().split(' ')
                # print(words)
                for w in words:
                    if w in word_count:
                        word_count[w] += 1
                    else:
                        word_count[w] = 1
        except:
            traceback.print_exc(file=sys.stderr)

    return word_count


