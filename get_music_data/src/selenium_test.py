# -*- coding: utf-8 -*-
__author__ = 'Kay'


import time
from selenium import webdriver

executable_path='/home/elastic/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')

# url = 'https://www.baidu.com/s?wd=selenium&rsv_spt=1&rsv_iqid=0xdfcd826000087a88&issp=1&f=3&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=4&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&prefixsug=sele&rsp=1&inputT=2422&rsv_sug4=2422&rsv_sug=2'
# url = 'http://music.163.com/#/user/home?id=88349979'
url = 'http://music.163.com/#/user/fans?id=61884303'
driver.get(url)
# driver.execute_script()
# time.sleep(3)
# re = driver.find_element_by_xpath('/html/body').text
driver.switch_to_frame('contentFrame')

# 微博ID获取
# re = driver.find_element_by_xpath('//*[@id="head-box"]/dd/div[4]/ul/li/a').get_attribute('href')
# print(re)


# 粉丝列表获取
for i in list(range(1, 21)):
    try:
        re = driver.find_element_by_xpath('//*[@id="main-box"]/li[{0}]/a'.format(str(i)))
        print(re.get_attribute('href').strip().split('id=')[1])
    except:
        print i, '< 20'
        break


# print(driver.get_screenshot_as_file('test'))
driver.close()


