#coding:utf-8
import traceback, sys
import datetime
# import MySQLdb as mysql
import pymysql as mysql


def get_keyword_id(word=None):
    list_id = []
    con = mysql.connect(host='192.168.1.101', charset='utf8', user='root', passwd='nlsde123!@#', db='wordemotion',
                        port=3306)
    cur = con.cursor()
    if word:
        sql = "select id from keywords where word='{}'".format(word)
        # print(sql)
        cur.execute(sql)
        rst = cur.fetchall()

    else:
        sql = 'select id from keywords'
        cur.execute(sql)
        rst = cur.fetchall()

    print('关键词个数:', len(rst))
    for row in rst:
        list_id.append(row[0])
    con.close()
    if len(list_id) == 1:
        return list_id[0]
    else:
        return list_id


def find(uid):
    try:
        con=mysql.connect(host='beihang1',charset='utf8',user='root',passwd='nlsde123!@#',db='weibousers',port=3306)
        cur=con.cursor()
        sql = "select id from users where uid='%s'" % uid
        cur.execute(sql)
        rst=cur.fetchall()
        id = -1
        for row in rst:
            id = row[0]
        cur.close()
        con.close()
        return id
    except:
        traceback.print_exc(file = sys.stderr)
        return -1


if __name__=='__main__':
    # print(find('1718735337'))
    print(get_keyword_id())
