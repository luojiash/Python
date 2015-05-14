#encoding: utf-8

import urllib2
from sys import stdout
import os
import socket
import threading

'''多线程下载文件，一个线程下载一个文件
每次创建 MAX_THREADS 个线程，等这批线程运行完后再创建下一批
下一版本将使用线程池
'''
MAX_THREADS = 20#最大线程数

class DownloadThread(threading.Thread):
    '''下载单个文件的线程'''
    def __init__(self, url, path):
        threading.Thread.__init__(self)
        self.url = url
        self.path = path
    
    def run(self):
        self.res = apply(self.download, (self.url, self.path))

    def getResult(self):
        return self.res
    
    def download(self, url, path):
        name = url[url.rindex('/')+1:]
        full_path = path + '/' + name
        if os.path.isfile(full_path):
            return '%s exists' %full_path
        try:
            resp = urllib2.urlopen(url, timeout=120)
            data = resp.read()
            resp.close()
            f = open(full_path, 'wb')
            f.write(data)
            f.close()
            return full_path + ' download succeed'
        except socket.timeout, e:
            return '*%s timeout' %url
        except Exception, e:
            return '*fail: %s %s' %(e, url)
            
            
def download(urls, path):
    if not os.path.exists(path):
        os.makedirs(path)
    
    size = len(urls)
    index = 0
    while index < size:
        threads = []
        for j in range(index, min(index+MAX_THREADS, size)):
            t = DownloadThread(urls[j], path)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
            print t.getResult()
        index += MAX_THREADS


