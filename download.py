#coding: utf8

from Queue import Queue
from sys import stdout
import urllib2
import os, time
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
                    stdout.write('\n*%s %s' % (e, urltp))
                    if not e.code == 404:
                        self.queue.put(urltp)
                except Exception, e:
                    stdout.write('\n*img2 %s' % e)
                    self.queue.put(urltp)
            self.queue.task_done()
