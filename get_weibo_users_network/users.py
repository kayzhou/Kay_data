#coding:utf-8
import datetime
import db_mysql
import db_hbase
import urllib2, urllib
import json
import traceback, sys

userinfo_url='http://beihang4:9999/queryWeiboUsers?type=2&'
friend_url='http://beihang4:9999/queryFriends?count=5000&userType=1&'


def crawl_insert(uid_list, log_f, table_name):
    tmp_follow_list = []
    step = 30
    for i in range(0, len(uid_list), step):
        try:
            slice_uid_list = uid_list[i: i+step]
            user_put_dict = {}
            user_params = 'users=%s' % ','.join(slice_uid_list)
            rst = urllib2.urlopen(userinfo_url + user_params, timeout = 50).read()
            user_list = json.loads(rst)
            name_id_dict = {}
            for user_info in user_list:
                try:
                    uid = user_info['id']
                    screen_name = user_info['screen_name'].encode('utf-8')
                    if screen_name:
                        user_put_dict[str(uid)] = {}
                        name_id_dict[screen_name] = str(uid)
                        user_put_dict[str(uid)]['u:json'] = json.dumps(user_info)
                except:
                    continue
            if name_id_dict:
                friend_params = 'users=%s' % (','.join(name_id_dict.keys()))
                rst = urllib2.urlopen(friend_url + friend_params, timeout = 50).read()
                user_friends_list = json.loads(rst)
                for user_friends in user_friends_list:
                    screen_name = user_friends['user'].encode('utf-8')
                    uid = name_id_dict[screen_name]
                    friends_list = user_friends['ids']
                    for friend_uid in friends_list:
                        user_put_dict[str(uid)]['u:'+str(friend_uid)] = '1'
        except:
            traceback.print_exc(file=sys.stderr)
        try:
            db_hbase.insert(user_put_dict, table_name)
            log_f.write('%s\t%s\t%s\t%s\n' % (datetime.datetime.now(), str(slice_uid_list), len(name_id_dict), len(slice_uid_list)))
            log_f.flush()
        except:
            traceback.print_exc(file=sys.stderr)
           

def get_sinceuid():
    fpath = 'since_uid'
    f = file(fpath)
    since_uid = int(f.read())
    f.close()
    return since_uid


def write_sinceuid(since_uid):
    fout = file('since_uid', 'w')
    fout.write(str(since_uid))
    fout.close()


def main():
    batch_user_cnt = 2000
    since_uid = get_sinceuid()
    log_f = file('crawl.log', 'a')
    table_name = 'users201411'
    while True:
        try:
            uid_list, since_uid = db_mysql.get_users(since_uid, batch_user_cnt)
            crawl_insert(uid_list, log_f, table_name)
            write_sinceuid(since_uid)
        except:
            traceback.print_exc(file=sys.stderr)
    log_f.close()


if __name__=='__main__':
    main()
