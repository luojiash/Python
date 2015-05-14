#encoding: utf-8

import urllib, urllib2
from urlparse import urlparse
from sys import stdout
import re, os
import socket
import traceback
import threading

import downloadutil
import downloadutil2
import downloadutil3

class mzitu():
    def __init__(self):
        p = r'http://pic.dofay.com/\d{4}/\d{2}/[\w-]+.(jpe?g|png)'
        self.imgPt = re.compile(p)
        self.titlePt = re.compile(r'<title>([^<]+)</title>')
        self.path = 'H:/_tmp'

    def getLink(self, url):
        resp = urllib2.urlopen(url)
        html = resp.read()
        reg = re.compile(r'href="(http://www.mzitu.com/\d+)"')
        
        index = 0
        f = open('H:/BaiduYunDownload/data1.txt', 'wb')
        while True:
            m = reg.search(html, index)
            if not m:
                break
            f.write('%s\n' % m.group(1))
            #print m.group(1)
            index = m.end(1)
        f.close()

    def getPath(self, url):
        '''get storage path'''
        parsedurl = urlparse(url)
        return self.path+'/'+parsedurl[1]+parsedurl[2]
    
    def _index(self, url):
        '''find max index'''
        resp = urllib2.urlopen(url)
        html = resp.read()
        resp.close()
        m = re.findall(r"href=['\"]"+url+"/(\d+)['\"]", html)
        if m:
            return max(int(s) for s in m)
        else:
            print "*find index fail: %s" % url
    
    def _m_index(self):
        m = re.search(r'/(\d+)页', self.html)
        if m:
            return int(m.group(1))
        else:
            print "*find index fail: %s" % url
    
    def getImgs(self, url):
        '''get img urls'''
        index = self._index(url)
        if not index:
            return
        
        #construct a img url list
        imgUrls = []
        for i in range(1, index + 1):
            urli = url+'/'+str(i)
            resp = urllib2.urlopen(urli)
            html = resp.read()
            resp.close()
            m = self.imgPt.search(html)
            if m:
                imgUrls.append(m.group())
            else:
                print "*find img fail: %s" %urli
        return imgUrls
        
        
    def m_getImgs(self, url, kw=None):
        url = url.replace('www', 'm')
        resp = urllib2.urlopen(url)
        self.html = resp.read()
        resp.close()
        
        if kw:
            m = self.titlePt.search(self.html)
            if m:
                if m.group(1).find(kw) != -1:
                    print '*%s in title' % kw
                    return
            else:
                print 'no title: %s' %url
    
        index = self._m_index()
        if not index:
            return
        
        #construct a img url list
        imgUrls = []
        for i in range(1, index + 1):
            urli = url+'/'+str(i)
            resp = urllib2.urlopen(urli)
            html = resp.read()
            resp.close()
            m = self.imgPt.search(html)
            if m:
                imgUrls.append(m.group())
            else:
                print "*find img fail: %s" %urli
        return imgUrls

def main(urllist):
    mzt = mzitu()
    d = downloadutil3.Downloader()
    for url in urllist:
        print url
        path = mzt.getPath(url)
        if os.path.exists(path):
            print '*%s exists\n' % path
            continue
        urls = mzt.m_getImgs(url, 'ROSI')
        if not urls: continue
        if not os.path.exists(path):
            os.makedirs(path)
        #downloadutil.download(mzt.imgUrls, mzt.getPath())
        #downloadutil2.main(urls, path)
        d.put([(url, path) for url in urls])
        print

s =''''''

urllist = s.split('\n')
main(urllist)
        
##mzt = mzitu()
##url = 'http://www.mzitu.com/all'
##mzt.getLink(url)
