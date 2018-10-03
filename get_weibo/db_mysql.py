#coding:utf-8
import MySQLdb

def select_keyword(keyword):
    con=MySQLdb.connect(host='beihang1',charset='utf8',user='root',passwd='nlsde123!@#',db='wordemotion',port=3306)
    cur=con.cursor()
    sql="select * from keywords where word='"+keyword+"'"
    cur.execute(sql)
    rst=cur.fetchall()
    return rst

if __name__=='__main__':
    print select_keyword('亚运会')
