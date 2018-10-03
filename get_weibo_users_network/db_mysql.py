#coding:utf-8
import traceback, sys
import MySQLdb
def get_users(since_uid, batch_user_cnt):
    con=MySQLdb.connect(host='beihang1',charset='utf8',user='root',passwd='nlsde123!@#',db='weibousers',port=3306)
    cur=con.cursor()
#    sql='select * from users limit 10'
#    sql="select * from users where uid='2920228750'"
    sql='select * from users where id>%s limit %s' % (since_uid, batch_user_cnt)
    cur.execute(sql)
    rst=cur.fetchall()
    uid_list = []
    max_user_index = -1
    for row in rst:
        try:
            user_index = row[0]
            uid=row[1]
            uid_list.append(str(uid))
            if user_index > max_user_index:
                max_user_index = user_index
        except:
            traceback.print_exc(file=sys.stderr)
    cur.close()
    con.close()
    return (uid_list, max_user_index)
