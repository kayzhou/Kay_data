# -*- coding: utf-8 -*-
__author__ = 'Kay'

import numpy as np
import matplotlib.pylab as plt
import matplotlib.dates as dts
import datetime


def strs2dates(strs):
    return [datetime.datetime.strptime(str(s), '%Y%m%d') for s in strs]


def loadtxt(in_name, y_index, x_index):
    y = []; x = []
    for line in open(in_name):
        data = line.strip().split(' ')
        y.append(data[y_index])
        x.append(data[x_index])
    return y, x


y, x = loadtxt('all_data.txt', 4, 0)
print y
print x
dates = strs2dates(x)
x = np.arange(len(y))

# 单图
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot_date(dates, y, 'b-', linewidth=1, alpha=0.8)
ax.grid()
ax.xaxis.set_major_locator(dts.MonthLocator())
ax.xaxis.set_major_formatter(dts.DateFormatter('%m\n%d'))
fig.suptitle('%s ~ %s' % (dates[0], dates[-1]), fontdict={'size': 16})
plt.ylabel('Amount')
plt.xlabel('Date')
fig.autofmt_xdate()
plt.show()

