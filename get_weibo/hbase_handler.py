# coding:utf-8
import happybase


def get_stock_hbase_con():
    return happybase.Connection('192.168.1.185')


def scan_tweet(table_name, start, stop):
    con = get_stock_hbase_con()
    table = con.table(table_name)
    rst = table.scan(row_start=start, row_stop=stop)
    tweet_list = []
    for key, data in rst:
        weiboid = key[15:]
        data['id'] = weiboid
        tweet_list.append(data)
    return tweet_list


if __name__ == '__main__':
    con = get_stock_hbase_con()
