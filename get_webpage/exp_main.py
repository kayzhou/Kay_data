#coding:utf-8
__author__ = 'Kay'
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import get_web_data
import json
import re


def get_exp_keyword():
    f = open("keyword.kay", "r")
    for line in f:
        print line[:-1]
    f.close()


# 删除换行,HTML标签
def delete_end_of_line(origin_str):
    if origin_str is None:
        return ""

    result_str = ""
    for line in origin_str.splitlines():
        result_str += line
    return re.sub('<[^>]+>', '', result_str)


def exp_main():
    # 打开关键词文件，进行行读取
    f = open("keyword.kay", "r")
    count = 0
    for line in f:
        count += 1
        # 去掉换行符
        word = line[:-1]
        print "count:", count, "word:", word
        # 从hbase中取出数据
        list_data = get_web_data.get_web_data(word, "2014120100", "2015020100", 2000)
        # 对文件准备进行写操作
        w_file = open("output/" + word + ".txt", "a")
        for data_dict in list_data:
            all_info_str = data_dict['w:']
            all_info_dict = json.loads(all_info_str)
            # 提取出网页数据中的标题和正文
            title = all_info_dict['fldtitle']
            content = delete_end_of_line(all_info_dict['Fldcontent'])
            # 写文件
	    # print title

	    if title is None: title = "null"
        if content is None: content = "null"

        w_file.write(title + " || " + content + "\n")


if __name__ == '__main__':
    exp_main()
