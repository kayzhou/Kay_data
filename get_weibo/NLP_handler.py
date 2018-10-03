#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import jieba
import os


def my_jieba_forfile(r_file_name, w_file_name):
    r_file = open(r_file_name, 'r')
    w_file = open(w_file_name, 'a')
    for line in r_file:
	seg_list = jieba.cut(line)
	seg_result = "/ ".join(seg_list)
	w_file.write(seg_result + '/n')


def all_file():
    count = 0
    for filename in os.listdir('weibo'):
	count += 1
	print "count:", count, "filename:", filename
        my_jieba_forfile("weibo/" + filename, "seg/" + filename)
 

if __name__ == "__main__":
    # my_jieba_forfile("output/周杰伦.txt","seg/周杰伦.txt")
    all_file()        
