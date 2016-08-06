# coding: utf-8

import os
import threading
from Queue import Queue
from sys import stdout, stderr

import requests

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'
}

class Downloader():

    def __init__(self, nthreads=24, headers=headers):
        self.queue = Queue()
        self.headers = headers
        for i in range(nthreads):
            t = DownloadThread(self)
            t.start()

    def add(self, url, path):
        self.queue.put((url, path))

    def join(self):
        self.queue.join()


class DownloadThread(threading.Thread):
    """下载单个文件的线程，守护线程，主进程结束后退出"""

    def __init__(self, dld):
        threading.Thread.__init__(self)
        self.dld = dld
        self.setDaemon(True)

    def run(self):
        queue = self.dld.queue
        headers = self.dld.headers
        while True:
            url, path = queue.get()
            stdout.write('%s ' % queue.unfinished_tasks)
            try:
                code = dl_img(url, path, headers)
                if code == 404:
                    stdout.write('%s %s\n' % (code, url))
                elif code != 200:
                    stderr.write('%s %s\n' % (code, url))
                    queue.put((url, path))
            except (requests.ReadTimeout, requests.ConnectionError) as e:
                stdout.write('%s %s\n' % (e, url))
                queue.put((url, path))
            except Exception as e:
                stderr.write('%s %s %s\n' % (type(e), e, url))
            queue.task_done()

def download(url, headers=headers, times=3):
    try:
        r = requests.get(url, headers=headers, timeout=64)
        return r.content
    except requests.ReadTimeout as e:
        if times == 0:
            raise e
        return download(url, headers, times-1)


def dl_img(url, path, headers=headers):
    if os.path.isfile(path):
        return 200
    r = requests.get(url, headers=headers, timeout=(16, 100))
    if r.status_code == 200:
        content = r.content
        with open(path, 'wb') as f:
            f.write(content)
    return r.status_code
