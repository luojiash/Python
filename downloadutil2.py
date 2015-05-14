#coding: utf8

from Queue import Queue
from sys import stdout
import urllib2
import os
import socket
import threading

class DownloadThread(threading.Thread):
    '''下载文件的一个线程'''
    def __init__(self, queue, path):
        threading.Thread.__init__(self)
        self.queue = queue
        self.path = path

    def run(self):
        while True:
            try:
                #exit thread when queue is empty
                url = self.queue.get(block=False)
            except Queue.Empty:
                break

            name = url[url.rindex('/')+1:]
            full_path = self.path + '/' + name
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
                except socket.timeout, e:
                    stdout.write('*%s timeout\n' %url)
                except Exception, e:
                    stdout.write('*Exception: %s %s\n' %(e, url))
            self.queue.task_done()



class Downloader():
    def __init__(self, urls, path, nthreads=20):
        self.queue = Queue(len(urls))
        for url in urls:
            self.queue.put(url)

        self.threads = []
        for i in range(nthreads):
            t = DownloadThread(self.queue, path)
            t.start()
            self.threads.append(t)
        
    def complete(self):
        self.queue.join()
        for thread in self.threads:
            if thread.isAlive():
                thread.join()

def main(urls, path):
    if not os.path.exists(path):
        os.makedirs(path)

    d = Downloader(urls, path)
    d.complete()
