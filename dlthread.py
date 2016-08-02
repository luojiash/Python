# coding: utf-8

import os
import socket
import threading
import urllib2
from sys import stdout, stderr

root_path = 'F:' + os.path.sep + 'tmp'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'
}

class Item:
    def __init__(self, path, url):
        self.path = path
        self.url = url


class DownloadThread(threading.Thread):
    """下载单个文件的线程，守护线程，主进程结束后退出"""

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.setDaemon(True)

    def run(self):
        while True:
            item = self.queue.get()
            stdout.write('%s ' % self.queue.unfinished_tasks)

            if os.path.isfile(item.path):
                pass
            # stdout.write('%s exists\n' %name)
            else:
                try:
                    req = urllib2.Request(item.url, headers=headers)
                    data = urllib2.urlopen(req, timeout=60).read()
                    f = open(item.path, 'wb')
                    f.write(data)
                    f.close()
                    # stdout.write('%s download succeed\n' % item.path)
                # except urllib2.HTTPError, e:
                #     stdout.write('\n%s %s' % (e, item.url))
                #     if not e.code == 404:
                #         self.queue.put(item)
                except socket.error as e:
                    stdout.write('%s %s\n' % (e, item.url))
                    self.queue.put(item)
                except urllib2.URLError as e:
                    if not (type(e) == urllib2.HTTPError and e.code == 404):
                        stdout.write('%s %s\n' % (e, item.url))
                        self.queue.put(item)
                except Exception as e:
                    stderr.write('%s %s %s\n' % (type(e), e, item.url))
            self.queue.task_done()
