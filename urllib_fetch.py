#encoding: utf-8

import os

import urllib
import urllib2
import re
import traceback
import downloadutil
    
def search(urllist, keyword):
    pattern = r'title="([^"]*?柯南[^"]*?\d{3}[^"]*?'+keyword+'[^"]*?)" target="_blank"><img'
    reg = re.compile(pattern)
    count = 0
    for url in urllist:
        try:
            resp = urllib2.urlopen(url)
            data = resp.read().decode('gbk').encode('utf8')
            m  = reg.findall(data)
            if m:
                print url
                for title in m:
                    print '\t',title.decode('utf8')
                    count += 1
        except Exception, e:
            print 'fetch error:', url
            traceback.print_exc()
    print count, 'match'
            
def findimglink(url):
    resp = urllib2.urlopen(url)
    data = resp.read()
    p = r'<img[^>]+src="(http://pic.dbmeizi.com[a-zA-z0-9/]+\.[a-zA-Z]+)"'
    m = re.findall(p, data)
    return list(set(m))

##urllist = []
##pre = 'http://www.narutom.com/cartoon/conan/index_'
##suf = '.html'
##for i in range(2, 43):
##    urllist.append(pre+str(i)+suf)
##search(urllist, '基德')

url = 'http://www.dbmeizi.com/img/rank'
l = findimglink(url)
loop = range(len(l))
for i in loop:
    l[i] = l[i].replace('/s_', '/', 1)
print 'begin download img',len(l)
downloadutil.download(l, 'f:/tmp/www.dbmeizi.com')
