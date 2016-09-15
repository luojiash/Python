# coding: utf-8
# <<<<<<< HEAD

# import re
# from Queue import Queue

# from bs4 import BeautifulSoup

# from dlthread import *

# =======
import os
import re
import threading
from Queue import Queue
from sys import stderr, stdout

import time
from bs4 import BeautifulSoup

import downloader

root_path = 'F:'+os.path.sep+'tmp'
# >>>>>>> xxx

class Zng(threading.Thread):
    web_prefix = 'http://www.zngirls.com'

# <<<<<<< HEAD
    # def __init__(self, queue, gids):
        # threading.Thread.__init__(self)
        # self.queue = queue
        # self.gids = gids

    # @staticmethod
    # def request(url):
        # req = urllib2.Request(url, headers=headers)
        # return urllib2.urlopen(req, timeout=60).read()

    # def get_page(self, url):
        # html = Zng.request(url)
# =======
    def __init__(self, type, arg):
        threading.Thread.__init__(self)
        self.type = type
        self.arg = arg

    def get_page(self, url):
        html = downloader.download(url)
# >>>>>>> xxx
        soup = BeautifulSoup(html)
        p = int(soup.find(id='pages').find_all(class_=False)[-1].get_text())
        return p

    def get_albums(self, url):
# <<<<<<< HEAD
        # html = Zng.request(url)
# =======
        html = downloader.download(url)
# >>>>>>> xxx
        soup = BeautifulSoup(html)
        albums_a = soup.find(id='photo_list').find_all(class_='caption')
        albums = ['%s%s' % (self.web_prefix, i['href']) for i in albums_a]
        return albums

# <<<<<<< HEAD
    # def girls(self, gids):
        # while gids:
            # gid = self.gids.pop(0)
# =======
    def girls(self, gids, dld):
        while gids:
            gid = gids.pop(0)
# >>>>>>> xxx
            try:
                main_page = self.web_prefix + '/girl/' + str(gid) + '/album/'
                albums = self.get_albums(main_page)
            except Exception as e:
                stderr.write('%s %s\n' % (e, gid))
                continue

            while albums:
                url = albums.pop(0)
                try:
# <<<<<<< HEAD
                    # self.a_album(url)
                # except Exception as e:
                    # stderr.write('%s %s\n' % (e, url))
        
    # def a_album(self, url):
        # stdout.write('%s start\n' % url)

        # html = Zng.request(url)
# =======
                    self.a_album(url, dld)
                except Exception as e:
                    stderr.write('%s %s\n' % (e, url))
        
    def a_album(self, url, dld):
        stdout.write('%s start\n' % url)

        html = downloader.download(url)
# >>>>>>> xxx
        soup = BeautifulSoup(html)
        
        p = soup.find(id='dinfo').find(style=True).get_text()
        img_count = int(re.match(r'\d+', p).group())
        first_img = soup.find(id='hgallery').find('img')['src']
        
        album_path = os.path.join(root_path, 'www.zngirls.com', re.search(r'\d+', url).group())
        if not os.path.exists(album_path):
            os.makedirs(album_path)
# <<<<<<< HEAD
        # self.queue.put(Item(os.path.join(album_path, '0.jpg'), first_img))
        # imgi = first_img.replace('0.jpg', '{:03d}.jpg')
        # for i in range(1, img_count):
            # item = Item(os.path.join(album_path, '{:03d}.jpg'.format(i)), imgi.format(i))
            # self.queue.put(item)
            # # print item.path, item.url

    # def run(self):
# ##        self.a_album('http://www.zngirls.com/g/19238/')
        # self.girls(self.gids)


# def main():
    # headers['Referer'] = 'http://www.zngirls.com'
    # gids = [20468]
    # queue = Queue()
    # zng = Zng(queue, gids)
    # zng.start()

    # nthreads = 26
    # for i in range(nthreads):
        # t = DownloadThread(queue)
        # t.start()
    # zng.join()
    # queue.join()


# if __name__ == '__main__':
    # main()
# =======
        dld.add(first_img, os.path.join(album_path, '0.jpg'))
        imgi = first_img.replace('0.jpg', '{:03d}.jpg')
        time.sleep(1)
        for i in range(1, img_count):
            dld.add(imgi.format(i), os.path.join(album_path, '{:03d}.jpg'.format(i)))

    def run(self):
        headers = downloader.headers.copy()
        headers['Referer'] = 'http://www.zngirls.com'
        dld = downloader.Downloader(headers=headers)
        if self.type == 'album':
            self.a_album(self.arg, dld)
        else:
            self.girls(self.arg, dld)
        dld.join()

if __name__ == '__main__':
    gids = [21946]
    url = 'http://www.zngirls.com/g/19791/'
    zng = Zng('gilrs', gids)
    # zng = Zng('album', url)
    zng.start()
    zng.join()
# >>>>>>> xxx
