#coding: utf8

from Queue import Queue
from sys import stdout
import urllib2
import os
import socket
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
            
            url = urltp[0]
            path = urltp[1]
            name = url[url.rindex('/')+1:]
            full_path = path + '/' + name
            if os.path.isfile(full_path):
                stdout.write('%s exists\n' %full_path)
            else:
                try:
                    resp = urllib2.urlopen(url, timeout=120)
                    data = resp.read()
                    resp.close()
                    f = open(full_path, 'wb')
                    f.write(data)
                    f.close()
                    #stdout.write('%s download succeed\n' %full_path)
                except socket.timeout, e:
                    stdout.write('*%s timeout\n' %url)
                except Exception, e:
                    stdout.write('*Exception: %s %s\n' %(e, url))
            self.queue.task_done()
            stdout.write('+%d' %self.queue.unfinished_tasks)


class Downloader():
    def __init__(self, nthreads=20):
        self.queue = Queue()
        self.threads = []
        for i in range(nthreads):
            t = DownloadThread(self.queue)
            self.threads.append(t)
            t.start()

    def put(self, urltps):
        for tp in urltps:
            self.queue.put(tp)
        self.queue.join()
