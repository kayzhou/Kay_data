# -*- coding: utf-8 -*-
__author__ = 'Kay'

import os


def count_lines(in_name):
    count = 0
    for line in open(in_name, 'rU'):
        count += 1
    return count


for f in os.listdir('weibo_0320'):
    print f, count_lines('weibo_0320/' + f)
