#encoding: utf-8

import urllib, urllib2
from urlparse import urlparse
from sys import stdout
from Queue import Queue
import re, os, time
import socket
import traceback
import threading

class DownloadThread(threading.Thread):
    '''下载单个文件的线程，守护线程，主进程结束后退出'''
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.setDaemon(True)

    def run(self):
        while True:
            urltp = self.queue.get()
            stdout.write('%s' % self.queue.unfinished_tasks)

            path = urltp[0]#storage path
            url = urltp[1]#img addr
            name = url[url.rindex('/')+1:]
            full_path = path + '/' + name
            if os.path.isfile(full_path): pass
                #stdout.write('%s exists\n' %name)
            else:
                try:
                    resp = urllib2.urlopen(url, timeout=60)
                    data = resp.read()
                    resp.close()
                    f = open(full_path, 'wb')
                    f.write(data)
                    f.close()
                    #stdout.write('%s download succeed\n' %full_path)
                except urllib2.HTTPError, e:
                    stdout.write('\n*img %s' % e)
                    if not e.code == 404:
                        self.queue.put(urltp)
                except Exception, e:
                    stdout.write('\n*img2 %s' % e)
                    self.queue.put(urltp)
            self.queue.task_done()

class mzitu(threading.Thread):
    def __init__(self, queue, urls, path):
        threading.Thread.__init__(self)
        self.queue = queue
        self.urls = urls
        self.path = path

    def get_storage_path(self, url):
        parsedurl = urlparse(url)
        return self.path+'/'+parsedurl[1]+parsedurl[2]

    def index(self, html):
        m = re.search(r'/(\d+)页', html)
        if m: return int(m.group(1))
        return 0

    def filter(self, html, kws = None):
        for kw in kws:
            p = r'<title>[^<]*'+kw+'[^<]*</title>'
            m = re.search(p, html)
            if m:
                print '%s in title' % kw
                return False
        return True

    def run(self):
        img_pt = re.compile(
            r'http://pic.dofay.com/\d{4}/\d{2}/[\w-]+.(jpe?g|png)')
        img_pt_ord = re.compile(
            r'http://pic.dofay.com/\d{4}/\d{2}/[\w-]+01.(jpe?g|png)')

        while self.urls:
            url = self.urls.pop(0)
            stdout.write('\n----%s start' % url)
            try:
                resp = urllib2.urlopen(url, timeout=30)
                html = resp.read()
                resp.close()
            except Exception, e:
                stdout.write('\n*%s %s' % (e, url))
                self.urls.append(url)
                continue

            #过滤标题关键字
            if not self.filter(html, ['ROSI']): continue

            index = self.index(html)
            if not index:
                stdout.write('\n*index fail %s' % url)
                continue

            path = self.get_storage_path(url)
            if not os.path.exists(path): os.makedirs(path)

            #construct img urls
            m = img_pt_ord.search(html)
            if m:
                imgi = m.group().replace('01.', '{:02d}.')
                for i in range(1, index+1):
                    self.queue.put((path, imgi.format(i)))
                continue

            urlis = []
            for i in range(1, index + 1):
                urlis.append(url+'/'+str(i))
            while urlis:
                urli = urlis.pop(0)
                try:
                    resp = urllib2.urlopen(urli, timeout=30)
                    html = resp.read()
                    resp.close()
                except Exception, e:
                    stdout.write('\n*%s %s' % (e, urli))
                    urlis.append(urli)
                    continue
                m = img_pt.search(html)
                if m:
                    self.queue.put((path, m.group()))
                else:
                    print "*find img fail: %s" %urli

def getLink(url):
    '''从一个页面获取页面链接'''
##    resp = urllib2.urlopen(url)
##    html = resp.read()
    html = open(u'E:/百度云同步盘/data1.txt').read()
    reg = re.compile(r'href="(http://m.mzitu.com/\d+)"')

    index = 0
    f = open('D:/tmp/data.txt', 'wb')
    while True:
        m = reg.search(html, index)
        if not m:
            break
        f.write('%s\n' % m.group(1))
        print m.group(1)
        index = m.end(1)
    f.close()

def main():
    s ='''http://m.mzitu.com/35719'''
    urllist = s.split('\n')
    for i in range(urllist.count('')):
        urllist.remove('')

    queue = Queue()
    mzt = mzitu(queue, urllist, 'D:/tmp')
    mzt.start()

    nthreads = 20
    for i in range(nthreads):
        t = DownloadThread(queue)
        t.start()
    mzt.join()
    queue.join()

if __name__ == '__main__':
    main()
