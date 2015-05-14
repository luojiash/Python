#encoding: utf-8

import os
import urllib2
import urllib
import re

def f1():
    p = r'(.+?\?.+)'
    reg = re.compile(p)

    f = open(r'H:\BaiduYunDownload\data.txt')
    urls = []
    for url in f.readlines():
        m = reg.match(url)
        if m:
            #print '"%s",' %m.group(1)
##            tmp = m.group(1).replace("www.", "m.")\
##                  .replace("localjoin-", "usa-localjoin-")
##            print 'urlAdapter.urlMap.put("%s", "%s");' %(m.group(1),tmp)
            urls.append(m.group(1))
    f.close()
    return urls

def visit(urls):
    headers = {'User-Agent': 'iPhone'}
    for url in urls:
        #url = urllib.quote(url, safe=r":/?=&")
        print url
        request = urllib2.Request(url, headers=headers)
        resp = urllib2.urlopen(request)
        print resp.geturl()
        print

urls = f1()
visit(urls)
