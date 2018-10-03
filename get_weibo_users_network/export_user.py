#coding:utf-8
import sys, traceback
import happybase
import random
host_list=['beihang1','beihang2','beihang3','beihang4','beihang5','beihang6','beihang7','beihang10','beihang11','beihang12','beihang13']
def get_hbase_con():
    while True:
        try:
            host=random.choice(host_list)
            con=happybase.Connection(host)
            return con
        except:
            traceback.print_exc(file=sys.stderr)
root = '/data1/user_relation/'
f_profile = file(root + 'users', 'w')
f_relation = file(root + 'relation', 'w')
row_start = '1'
row_stop = '9999999999999999999999'
max_key = row_start
cnt = 0
while row_start < row_stop:
    uid_list = []
    try:
        conn = get_hbase_con()
        table = conn.table('users201411')
        for key, data in table.scan(row_start = max_key, row_stop = row_stop, limit = 500):
            uid = key
            if uid > max_key:
                max_key = uid
            uid_list.append(uid)
            follow_list = []
            profile = ''
            for field in data:
                k = field.split(':')[1]
                if k.isdigit():
                    follow_list.append(k)
                elif k == 'json':
                    profile = data[field]
            follow_str = ' '.join(follow_list)
            f_relation.write('%s|**|%s\n' % (uid, follow_str))
            f_profile.write('%s\n' % profile)
        if not uid_list:
            break
        max_key = str(int(max_key) + 1)
    except:
        traceback.print_exc(file = sys.stderr)
    conn.close()
    '''
    if cnt >= 2:
        break
    cnt += 1
    '''
f_profile.close()
f_relation.close()
