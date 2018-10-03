#coding:utf-8
#__author__ = 'Kay'

import urllib
import json
from dateutil.relativedelta import *
import datetime
import mysql_handler
import hbase_handler
import time
import sys

# datetime -> timestamp
def datetime_to_stamp(t):
    return time.mktime(t.timetuple())

# hbase_id格式
# str(keyword_id).zfill(5) + timeStamp + str(h_current_id).zfill(16)
# timestamp = str(time.mktime(datetime.timetuple()))[:-2].zfill(10)

# 网站数据下载接口
def get_web_data(keyword, start, end, cnt_limit):
    
    '''
    input: 
        四个参数均为string类型
        keyword:关键字
        start:数据的起始时间，格式为'%Y%m%d%H'
        end:数据的终止时间，格式为'%Y%m%d%H'
        cnt_limit:下载限制数目
    
    print:
        显示：每行表示一条数据，每条数据为Json的形式
        具体形式如下：
        # 新闻、博客和论坛
        data['datatype'] = datatype
        # 数字ID
        data['fldRecdId'] = row[0]; id = row[0]
        # 频道ID
        data['fldItemId'] = row[1]
        # URL地址
        data['fldUrlAddr'] = row[2]
        # 入口地址
        data['fldrkdz'] = row[3]
        # 频道路径
        data['pdmc'] = row[4]
        # 所属网站
        data['webname'] = row[5]
        # 标题    
        data['fldtitle'] = row[6]
        # 作者
        data['fldAuthor'] = row[7]
        # 正文内容
        data['Fldcontent'] = row[8]
        # 发布时间
        data['fldrecddate'] = row[9]
        # 点击数
        data['fldHits'] = row[10]
        # 回复数
        data['fldReply'] = row[11]
    '''
    rst = mysql_handler.select_keyword(keyword)
    if len(rst) == 0:
        print '没有该关键词', keyword
        return {}
    keyword_id = -1
    for row in rst:
        keyword_id = row[0]
    if keyword_id == -1:
        print '没有该关键词', keyword
        return {}
        
    start_time = datetime.datetime.strptime(start, '%Y%m%d%H')
    start_stamp = datetime_to_stamp(start_time)
    end_time = datetime.datetime.strptime(end, '%Y%m%d%H')
    end_stamp = datetime_to_stamp(end_time)
    start = str(keyword_id).zfill(5) + str(int(start_stamp)).zfill(10) + '0000000000000000'
    end = str(keyword_id).zfill(5) + str(int(end_stamp)).zfill(10) + '0000000000000000'
    table_name = 'webpage_keydata'
    if cnt_limit == 0:
        tweet_list = hbase_handler.scan_tweet_nolimit(table_name, start, end)
    else:
        tweet_list = hbase_handler.scan_tweet(table_name, start, end, int(cnt_limit))
    return tweet_list

    # print data['w:']
    # dict_str = json.loads(data['w:'])
    # print dict_str
    # 标题
    # print dict_str['fldtitle']
    # 正文
    # print dict_str["Fldcontent"]
    # 作者
    # print dict_str["fldAuthor"]
    # 发布时间
    # print dict_str['fldrecddate']
    # 网站
    # print dict_str["webname"]
    # 来源类型
    # print dict_str['datatype']
    # 超链接
    # print dict_str["fldUrlAddr"]

if __name__ == "__main__":
    # keyword = '股票||股市||证券||上证指数||深成指||成分指数'
    # start = '2014120100'
    # end = '2015010100'
    # cnt_limit = 10

    keyword = sys.argv[1]
    start = sys.argv[2]
    end = sys.argv[3]
    cnt_limit = sys.argv[4]

    # 处理或逻辑
    list_web_data = []
    list_keyword = keyword.split("||")
    for kw in list_keyword:
        list_web_data += get_web_data(kw, start, end, cnt_limit)
    print list_web_data

    # get_web_data('北航', '2014120100', '2015013100', 10)
