#coding:utf-8
import traceback, sys
import random
import happybase
host_list=['beihang1','beihang2','beihang3','beihang4','beihang5','beihang6','beihang7','beihang10','beihang11','beihang12','beihang13']
def get_hbase_con():
    while True:
        try:
            host=random.choice(host_list)
            con=happybase.Connection(host)
            return con
        except:
            traceback.print_exc(file=sys.stderr)
def insert(rowkey_putdict, table_name):
    con=get_hbase_con()
    table = con.table(table_name)
    batch = table.batch()
    for rowkey in rowkey_putdict:
        put_dict = rowkey_putdict[rowkey]
        batch.put(rowkey, put_dict)
    batch.send()
