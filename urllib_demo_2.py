#encoding:utf-8

import urllib.request
import http.cookiejar
import re

import FileUtil

'''发送header伪装浏览器
'''
def make_opener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        header.append((key, value))
    opener.addheaders = header
    return opener

url = 'http://www.baidu.com'
opener = make_opener()
rsp = opener.open(url, timeout = 1000)
data = rsp.read()
FileUtil.save("D:/urlopen.html", data)

