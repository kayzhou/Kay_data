# -*- coding: utf-8 -*-
__author__ = 'Kay'

import json, csv, sys, os
from datetime import datetime
from dateutil.parser import parse
from xlwt import Workbook


def get_uname_uid_mapping(in_name):
    '''
    读取用户名和用户ID的映射
    :param in_name:
    :return:
    '''
    mapp = {}
    for line in open(in_name):
        uName, uid = line.strip().split(',')
        mapp[uid] = uName
    return mapp


def convert(csv_file, json_file, col_list):
    csv_out = csv.writer(open(csv_file, "w"))
    # csv_out.writerow(col_list)
    csv_out.writerow(["创建时间", "微博ID", "转发数", "评论数", "点赞数", "微博内容"])

    list_json = [json.loads(line.strip()) for line in open(json_file)]


    for js in list_json:
        write = 1
        for col in col_list:
            if col == "created_at":
                pDate = parse(js[col])
                print(pDate.year, pDate.month)

                if pDate.year != 2016 or pDate.month != 7:
                    write = 0

                if pDate < datetime(2016, 7, 1):
                    break
                js[col] = pDate.strftime("%Y-%m-%d %H:%M:%S")

        if write:
            csv_out.writerow([js[col] for col in col_list])


def convert_excel(json_file, xls_file, col_list):
    book = Workbook(encoding='utf8')
    sheet = book.add_sheet('data')
    sheet.write(0, 0, '时间')
    sheet.write(0, 1, '微博id')
    sheet.write(0, 2, '转发数')
    sheet.write(0, 3, '评论数')
    sheet.write(0, 4, '点赞数')
    sheet.write(0, 5, '微博内容')

    list_json = [json.loads(line.strip()) for line in open(json_file)]

    for i, js in enumerate(list_json):
        for col in col_list:
            if col == "created_at":
                pDate = parse(js[col])

                # 过滤时间
                if pDate.year != 2016 or pDate.month != 7: break
                js[col] = pDate.strftime("%Y-%m-%d %H:%M:%S")

        row = [js[col] for col in col_list]
        for j, r in enumerate(row):
            sheet.write(i + 1, j, r)

    book.save(xls_file)


if __name__ == '__main__':
    col_list = ["created_at",
                # "screen_name",
                "id",
                "reposts_count",
                "comments_count",
                "attitudes_count",
                "text"]

    mapp = get_uname_uid_mapping('mapp.txt')
    di = sys.argv[1]
    for fi in os.listdir(di):
        if fi == 'csv': 
            continue
        print(os.path.join(di, fi))
        # convert(os.path.join(di, fi), os.path.join(di + "/csv", fi + '.txt'), col_list)
        uName = mapp[fi]
        convert_excel(os.path.join(di, fi), os.path.join(di + "/csv", uName + '.xls'), col_list)
