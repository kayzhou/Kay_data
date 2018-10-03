__author__ = 'Kay Zhou'

'''
统计/data2/uid_name中的数据
'''
import datetime


def count_lines(in_name):
    lines = open(in_name).readlines()
    print(len(lines))
    return len(lines)


def add_day(str_datetime, n=1, rule='%Y-%m-%d'):
    '''
    :param str_datetime: 时间字符串
    :return: +n day 时间字符串
    '''
    dt = datetime.datetime.strptime(str_datetime, rule)
    time_delta = datetime.timedelta(days=n)
    dt = dt + time_delta
    return dt.strftime(rule)


def add_month(s):
    month = int(s[-2:])
    year = int(s[:-2])
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return str(year) + str(month).zfill(2)


if __name__ == '__main__':
    # count_lines('stat_users.py')

    # 统计月
    # start = '201409'
    # end = '201701'
    # dt = start
    #
    # x = []
    # y = []
    # out_file = open(start + '-' + end, 'w')
    # while dt < end:
    #     print(dt)
    #     x.append(dt)
    #     count = count_lines('/data2/uid_name/%s-%s.txt' % (dt[:4], dt[-2:]))
    #     y.append(count)
    #     out_file.write(dt + ',' + str(count) + '\n')
    #     dt = add_month(dt)
    # out_file.close()


    # 统计日
    start = '2014-09-01'
    end = '2017-02-01'
    dt = start

    x = []
    y = []
    out_file = open(start + '-' + end + '.csv', 'w')
    while dt < end:
        print(dt)
        x.append(dt)
        count = count_lines('data/uid_name/%s_uid_name.txt' % dt.replace('-', ''))
        y.append(count)
        out_file.write(dt + ',' + str(count) + '\n')
        dt = add_day(dt)
    out_file.close()