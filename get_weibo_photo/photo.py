import datetime
import json
import re
import time
import random

import pymongo as pm
from selenium import webdriver
driver = webdriver.PhantomJS(executable_path=
                             '../phantomjs-2.1.1-macosx/bin/phantomjs')

url='https://weibo.com/u/1164286974?is_hot=1'
driver.get(url)
# print(driver.find_element_by_xpath('//*[@id="Pl_Official_Headerv6__1"]/div[1]/div/div[2]/div[1]/p/img'))


