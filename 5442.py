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

from bs4 import BeautifulSoup

import downloader

root_path = 'F:'+os.path.sep+'tmp'
# >>>>>>> xxx

class F442(threading.Thread):
    pt = re.compile(r'(\d+)')

# <<<<<<< HEAD
    # def __init__(self, urls, queue):
        # threading.Thread.__init__(self)
        # self.urls = urls
        # self.queue = queue

    # @staticmethod
    # def img_pt(m):
        # if m.group(1) == '':
# =======
    def __init__(self, urls):
        threading.Thread.__init__(self)
        self.urls = urls

    @staticmethod
    def img_pt(m):
        if len(m.group(1)) == 1:
# >>>>>>> xxx
            return r'{:d}' + m.group(2)
        else:
            return r'{:02d}' + m.group(2)

    def run(self):
# <<<<<<< HEAD
        # for url in self.urls:
            # resp = urllib2.urlopen(url)
            # html = resp.read()
            # resp.close()
# =======
        downloader.headers['Referer'] = 'http://www.5442.com'
        dler = downloader.Downloader()
        for url in self.urls:
            html = downloader.download(url)
# >>>>>>> xxx

            soup = BeautifulSoup(html)
            img_url = soup.find(id='contents').find('img')['src']
            page_text = soup.find(id='aplist').find('a').get_text()
            img_count = int(F442.pt.search(page_text).group()) * 2
            print img_url, img_count

# <<<<<<< HEAD
            # img_url_fmt = re.sub(r'(0?)\d(\.\w{3}!)', F442.img_pt, img_url)
# =======
            i = re.search(r'(\d+)\.\w{3}!', img_url).group(1)
            start = int(i) # 图片开始下标
            img_url_fmt = re.sub(r'(\d+)(\.\w{3}!)', F442.img_pt, img_url)
# >>>>>>> xxx
            path = url[url.index('meinv') + 6:url.rindex('.')].replace('/', '_')
            path = os.path.join(root_path, 'www.5442.com', path)
            if not os.path.exists(path):
                os.makedirs(path)

# <<<<<<< HEAD
            # for i in range(1, img_count + 1):
                # item = Item(os.path.join(path, '%s.jpg' % i), img_url_fmt.format(i))
                # self.queue.put(item)

# if __name__ == '__main__':
    # queue = Queue()
    # urls = ['http://www.5442.com/meinv/20160623/32951.html']
    # f442 = F442(urls, queue)
    # f442.start()

    # for i in range(128):
        # DownloadThread(queue).start()
    # f442.join()
    # queue.join()
# =======
            for i in range(start, start + img_count):
                dler.add(img_url_fmt.format(i), os.path.join(path, '%s.jpg' % i))
        dler.join()

if __name__ == '__main__':
    urls = ['http://www.5442.com/meinv/20160823/34969.html',
            'http://www.5442.com/meinv/20160825/35055.html',
            'http://www.5442.com/meinv/20160831/35247.html']
    f442 = F442(urls)
    f442.start()
    f442.join()

# >>>>>>> xxx
