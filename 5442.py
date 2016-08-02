# coding: utf-8
import re
from Queue import Queue

from bs4 import BeautifulSoup

from dlthread import *


class F442(threading.Thread):
    pt = re.compile(r'(\d+)')

    def __init__(self, urls, queue):
        threading.Thread.__init__(self)
        self.urls = urls
        self.queue = queue

    @staticmethod
    def img_pt(m):
        if m.group(1) == '':
            return r'{:d}' + m.group(2)
        else:
            return r'{:02d}' + m.group(2)

    def run(self):
        for url in self.urls:
            resp = urllib2.urlopen(url)
            html = resp.read()
            resp.close()

            soup = BeautifulSoup(html)
            img_url = soup.find(id='contents').find('img')['src']
            page_text = soup.find(id='aplist').find('a').get_text()
            img_count = int(F442.pt.search(page_text).group()) * 2
            print img_url, img_count

            img_url_fmt = re.sub(r'(0?)\d(\.\w{3}!)', F442.img_pt, img_url)
            path = url[url.index('meinv') + 6:url.rindex('.')].replace('/', '_')
            path = os.path.join(root_path, 'www.5442.com', path)
            if not os.path.exists(path):
                os.makedirs(path)

            for i in range(1, img_count + 1):
                item = Item(os.path.join(path, '%s.jpg' % i), img_url_fmt.format(i))
                self.queue.put(item)

if __name__ == '__main__':
    queue = Queue()
    urls = ['http://www.5442.com/meinv/20160623/32951.html']
    f442 = F442(urls, queue)
    f442.start()

    for i in range(128):
        DownloadThread(queue).start()
    f442.join()
    queue.join()
