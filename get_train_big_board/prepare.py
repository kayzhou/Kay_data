# -*- coding: utf-8 -*-
__author__ = 'Kay'

def load_history(fi_name):
    history = dict()
    fi = open(fi_name)
    for line in fi.readlines():
        line = line.strip()
        re = line.split('\t')
        history[re[0]] = re[1:]
    return history

his = load_history('/Users/Kay/Project/EXP/big_board/get_train_big_board/data/2014-2015_real.txt')
print his['2015/1/5']