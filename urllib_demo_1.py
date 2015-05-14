#encoding:utf-8

import urllib.request
import re
from collections import deque
'''deque, set 抓取网页
'''
queue = deque()
visited = set()

root_url = "http://news.dbanotes.net"
queue.append(root_url)

cnt = 0
while queue:
    url = queue.popleft()
    visited.add(url)
    print('已经抓取: ' + str(cnt) + '   正在抓取 <---  ' + url)
    cnt += 1

    try:
        rsp = urllib.request.urlopen(url, timeout = 2)
    except:
        print('连接错误 xxxxx '， url)
    if 'html' not in rsp.getheader('Content-Type'):
        continue
    try:
        data = rsp.read().decode('utf-8')
    except:
        continue

    linkre = re.compile('href="(.+?)"')
    for x in linkre.findall(data):
        if 'http' in x and x not in visited:
            queue.append(x)
            print('加入队列 --->  ' + x)
    
    
