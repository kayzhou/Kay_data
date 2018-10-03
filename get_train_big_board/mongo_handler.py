#coding:utf-8
__author__ = 'Kay'

import pymongo

def get_stock_db():
    mongo_con = 'mongodb://beihang9:27017'
    return pymongo.MongoClient(mongo_con).stock


def get_stock_coll():
    mongo_con = 'mongodb://beihang9:27017'
    return pymongo.MongoClient(mongo_con).stock.stock_v2
