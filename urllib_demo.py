#encoding: utf-8

import os

import urllib
import urllib2
import re
import traceback

def test():
    param = {'wd': '百度'};
    url = 'http://www.baidu.com/s?' + urllib.urlencode(param)
    resp = urllib2.urlopen(url)
    data = resp.read()
    if data.find('以下图片可能让您感觉不适') > 0:
        print '----' * 4
        
def test1():
    url = 'http://www.zhihu.com/notifications'
    resp = urllib2.urlopen(url)
    print resp.geturl()
    print resp.info()
    print resp.getcode()

test1()
