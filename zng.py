#coding: utf-8

import urllib, urllib2
from bs4 import BeautifulSoup
from sys import stdout, stderr
import os
from Queue import Queue
import threading
import re

from download import DownloadThread

class Zng(threading.Thread):
    max_page = 1000
    img_prefix = 'http://img.zngirls.com/gallery'
    web_prefix = 'http://www.zngirls.com'

    def __init__(self, queue, path, gids):
        threading.Thread.__init__(self)
        self.queue = queue
        self.path = path
        self.gids = gids

    def get_page(self, url):
        tmp = '%s%s.html' % (url, self.max_page)
        resp = urllib2.urlopen(url, timeout=30)
        html = resp.read()
        resp.close()
        soup = BeautifulSoup(html)
        p = int(soup.find(id='pages').find_all(class_=False)[-1].get_text())
        return p

    def get_img_count(self, url):
        tmp = '%s%s.html' % (url, self.max_page)
        resp = urllib2.urlopen(url, timeout=30)
        html = resp.read()
        resp.close()
        soup = BeautifulSoup(html)
        p = soup.find(id='dinfo').find(style=True).get_text()
        m = re.match(r'\d+', p)
        if m:
            return int(m.group())
        return 0

    def get_albums(self, url):
        resp = urllib2.urlopen(url, timeout=30)
        html = resp.read()
        resp.close()
        soup = BeautifulSoup(html)
        albums_a = soup.find(id='photo_list').find_all(class_='caption')
        albums = ['%s%s' % (self.web_prefix, i['href']) for i in albums_a]
        return albums

    def run(self):
        while self.gids:
            gid = self.gids.pop(0)
            try:
                main_page = self.web_prefix+'/girl/'+str(gid)+'/album/'
                albums = self.get_albums(main_page)
            except Exception, e:
                stdout.write('\n*%s %s' % (e, gid))
                self.gids.append(gid)
                continue

            while albums:
                url = albums.pop(0)
                stdout.write('\n---%s start' % url)
                try:
                    img_count = self.get_img_count(url)
                    if img_count == 0:
                        stderr.write('\n*%s get_img_count fail' % url)
                        continue
                except Exception, e:
                    stdout.write('\n*%s %s' % (e, url))
                    albums.append(url)
                    continue

                album_id = re.search(r'\d+', url).group()
                album_path = '%s/%s' % (self.path, album_id)
                if not os.path.exists(album_path): os.makedirs(album_path)

                first_img = '%s/%s/%s/0.jpg' % (self.img_prefix,gid,album_id)
                self.queue.put((album_path, first_img))
                imgi = '%s/%s/%s/{:03d}.jpg' % (self.img_prefix,gid,album_id)
                for i in range(1, img_count):
                    self.queue.put((album_path, imgi.format(i)))

def main():
    gids = [16930]
    queue = Queue()
    zng = Zng(queue, 'D:/tmp/www.zngirls.com', gids)
    zng.start()

    nthreads = 20
    for i in range(nthreads):
        t = DownloadThread(queue)
        t.start()
    zng.join()
    queue.join()

if __name__ == '__main__':
    main()
