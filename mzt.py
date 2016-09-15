#encoding: utf-8

# <<<<<<< HEAD
# import urllib, urllib2
# from urlparse import urlparse
# from sys import stdout
# from Queue import Queue
# import re, os, time
# import socket
# import traceback
# import threading

# from download import DownloadThread

# class mzitu(threading.Thread):
    # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'}
    # img_pre = 'http://img.dofay.com'

    # def __init__(self, queue, urls, path):
        # threading.Thread.__init__(self)
        # self.queue = queue
        # self.urls = urls
        # self.path = path

    # def get_storage_path(self, url):
        # parsedurl = urlparse(url)
        # return self.path+'/'+parsedurl[1]+parsedurl[2]

    # def index(self, html):
        # m = re.search(r'/(\d+)页', html)
        # if m: return int(m.group(1))
        # return 0
# =======
import os
import re
import threading
from sys import stdout, stderr
from urlparse import urlparse

from bs4 import BeautifulSoup

import downloader

root_path = 'F:'+os.path.sep+'tmp'

class mzitu(threading.Thread):
    img_pre = 'http://img.dofay.com'

    def __init__(self, urls):
        threading.Thread.__init__(self)
        self.urls = urls

    def get_storage_path(self, url):
        parsedurl = urlparse(url)
        return os.path.join(root_path,parsedurl[1],parsedurl[2][1:])
# >>>>>>> xxx

    def filter(self, html, kws = None):
        for kw in kws:
            p = r'<title>[^<]*'+kw+'[^<]*</title>'
            m = re.search(p, html)
            if m:
# <<<<<<< HEAD
                # print '%s in title' % kw
# =======
                stdout.write('%s in title' % kw)
# >>>>>>> xxx
                return False
        return True

    def run(self):
# <<<<<<< HEAD
        # img_pt = re.compile(self.img_pre + r'/\d{4}/\d{2}/[\w-]+.(jpe?g|png)')
        # img_pt_ord = re.compile(self.img_pre +
                                # r'/\d{4}/\d{2}/[\w-]+01.(jpe?g|png)')

        # while self.urls:
            # url = self.urls.pop(0)
            # stdout.write('\n----%s start' % url)
            # try:
                # req = urllib2.Request(url, headers=self.headers)
                # resp = urllib2.urlopen(req, timeout=30)
                # html = resp.read()
                # resp.close()
            # except Exception, e:
                # stdout.write('\n*%s %s' % (e, url))
# =======
        dld = downloader.Downloader()
        while self.urls:
            url = self.urls.pop(0)
            try:
                html = downloader.download(url)
            except Exception as e:
                stdout.write('%s %s\n' % (e, url))
# >>>>>>> xxx
                self.urls.append(url)
                continue

            #过滤标题关键字
            if not self.filter(html, ['ROSI']): continue

# <<<<<<< HEAD
            # index = self.index(html)
            # if not index:
                # stdout.write('\n*index fail %s' % url)
                # continue
# =======
            soup = BeautifulSoup(html)
            index = soup.select('.pagenavi a')[-2].find('span').getText()
            index = int(index)
            stdout.write('%s %s\n' % (url, index))
# >>>>>>> xxx

            path = self.get_storage_path(url)
            if not os.path.exists(path): os.makedirs(path)

            #construct img urls
# <<<<<<< HEAD
            # m = img_pt_ord.search(html)
            # if m:
                # imgi = m.group().replace('01.', '{:02d}.')
                # for i in range(1, index+1):
                    # self.queue.put((path, imgi.format(i)), True)
                # continue

            # urlis = []
            # for i in range(1, index + 1):
                # urlis.append(url+'/'+str(i))
            # while urlis:
                # urli = urlis.pop(0)
                # try:
                    # req = urllib2.Request(urli, headers=self.headers)
                    # resp = urllib2.urlopen(req, timeout=30)
                    # html = resp.read()
                    # resp.close()
                # except Exception, e:
                    # stdout.write('\n*%s %s' % (e, urli))
                    # urlis.append(urli)
                    # continue
                # m = img_pt.search(html)
                # if m:
                    # self.queue.put((path, m.group()), True)
                # else:
                    # print "*find img fail: %s" %urli

# def getLink(url):
    # '''从一个页面获取页面链接'''
# ##    req = urllib2.Request(url, headers=mzitu.headers)
# ##    resp = urllib2.urlopen(req)
# ##    html = resp.read()
# ##    resp.close()
    # html = open(u'E:/百度云同步盘/data1.txt').read()
    # reg = re.compile(r'href="(http://www\.fmeizi\.com/\d+)"')

    # index = 0
    # f = open('D:/tmp/data.txt', 'wb')
    # while True:
        # m = reg.search(html, index)
        # if not m:
            # break
        # f.write('%s\n' % m.group(1))
        # print m.group(1)
        # index = m.end(1)
    # f.close()

# def main():
    # s ='''http://m.mzitu.com/44836'''
    # urllist = s.split('\n')
    # for i in range(urllist.count('')):
        # urllist.remove('')

    # queue = Queue(100)
    # mzt = mzitu(queue, urllist, 'D:/tmp')
    # mzt.start()

    # nthreads = 20
    # for i in range(nthreads):
        # t = DownloadThread(queue)
        # t.start()
    # mzt.join()
    # queue.join()

# if __name__ == '__main__':
    # main()
# =======
            first = soup.find(class_='main-image').find('img')['src']
            img_fmt = first.replace('01.', '{:02d}.')
            for i in range(1, index+1):
                img_i = img_fmt.format(i)
                dld.add(img_i, os.path.join(path, img_i[img_i.rindex('/')+1:]))
        dld.join()

if __name__ == '__main__':
    urllist = [
        'http://www.mzitu.com/72325',
        'http://www.mzitu.com/72264',
        'http://www.mzitu.com/72036',
        'http://www.mzitu.com/71235',
        'http://www.mzitu.com/71110',
        'http://www.mzitu.com/71176',
        'http://www.mzitu.com/71439'
    ]
    mzt = mzitu(urllist)
    mzt.start()
    mzt.join()
# >>>>>>> xxx
