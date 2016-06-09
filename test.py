#coding: utf-8

import urllib2, time, os, re
from urlparse import urlparse
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
from Queue import Queue

from download import DownloadThread

class A:
    __metaclass__ = ABCMeta
    @abstractmethod
    def method(self):
        pass

class B:
    a = 1
    def p(self):
        print self.a, B.a

class Indexer:
    data = [5,6,7,8,9]
    def __getitem__(self, index):
        print index, self.data[index]

def f():
    html = '''<div id="photo_list"><ul class="photo_ul"><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/13545/"><img alt="刘飞儿Faye-泰国Pai县第三套写真 [秀人网XIUREN]" src="http://img.zngirls.com/gallery/19705/13545/cover/0.jpg" title="刘飞儿Faye-泰国Pai县第三套写真 [秀人网XIUREN]"></a></div><div class="igalleryli_title"><a href="/g/13545/" class="caption">刘飞儿Faye-泰国Pai县第三套写真 [秀人网XIUREN]</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/13286/"><img alt="刘飞儿Faye-性感主题拍摄宝贝私房写真 [TGOD推女神]" src="http://img.zngirls.com/gallery/19705/13286/cover/0.jpg" title="刘飞儿Faye-性感主题拍摄宝贝私房写真 [TGOD推女神]"></a></div><div class="igalleryli_title"><a href="/g/13286/" class="caption">刘飞儿Faye-性感主题拍摄宝贝私房写真 [TGOD推女神]</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/13266/"><img alt="刘飞儿Faye-《女神去哪儿》第20期 [TGOD推女神]" src="http://img.zngirls.com/gallery/19705/13266/cover/0.jpg" title="刘飞儿Faye-《女神去哪儿》第20期 [TGOD推女神]"></a></div><div class="igalleryli_title"><a href="/g/13266/" class="caption">刘飞儿Faye-《女神去哪儿》第20期 [TGOD推女神]</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/13128/"><img alt="刘飞儿Faye-[MyGirl美媛馆]Vol.078" src="http://img.zngirls.com/gallery/19705/13128/cover/0.jpg" title="刘飞儿Faye-[MyGirl美媛馆]Vol.078"></a></div><div class="igalleryli_title"><a href="/g/13128/" class="caption">刘飞儿Faye-[MyGirl美媛馆]Vol.078</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/13050/"><img alt="刘飞儿Faye-泰国Pai县写真 [XIUREN秀人网]" src="http://img.zngirls.com/gallery/19705/13050/cover/0.jpg" title="刘飞儿Faye-泰国Pai县写真 [XIUREN秀人网]"></a></div><div class="igalleryli_title"><a href="/g/13050/" class="caption">刘飞儿Faye-泰国Pai县写真 [XIUREN秀人网]</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/13045/"><img alt="刘飞儿Faye-泰国清迈旅拍第一套写真 [秀人网美媛馆]" src="http://img.zngirls.com/gallery/19705/13045/cover/0.jpg" title="刘飞儿Faye-泰国清迈旅拍第一套写真 [秀人网美媛馆]"></a></div><div class="igalleryli_title"><a href="/g/13045/" class="caption">刘飞儿Faye-泰国清迈旅拍第一套写真 [秀人网美媛馆]</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/12797/"><img alt="刘飞儿Faye-[秀人网]美媛馆 XR20150113N00280" src="http://img.zngirls.com/gallery/19705/12797/cover/0.jpg" title="刘飞儿Faye-[秀人网]美媛馆 XR20150113N00280"></a></div><div class="igalleryli_title"><a href="/g/12797/" class="caption">刘飞儿Faye-[秀人网]美媛馆 XR20150113N00280</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/12786/"><img alt="刘飞儿Faye-泰国写真[XIUREN秀人网]XR20141228N00262" src="http://img.zngirls.com/gallery/19705/12786/cover/0.jpg" title="刘飞儿Faye-泰国写真[XIUREN秀人网]XR20141228N00262"></a></div><div class="igalleryli_title"><a href="/g/12786/" class="caption">刘飞儿Faye-泰国写真[XIUREN秀人网]XR20141228N00262</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/12752/"><img alt="刘飞儿Faye-厦门鼓浪屿旅拍写真[秀人网] XR20141110N00237" src="http://img.zngirls.com/gallery/19705/12752/cover/0.jpg" title="刘飞儿Faye-厦门鼓浪屿旅拍写真[秀人网] XR20141110N00237"></a></div><div class="igalleryli_title"><a href="/g/12752/" class="caption">刘飞儿Faye-厦门鼓浪屿旅拍写真[秀人网] XR20141110N00237</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/11564/"><img alt="刘飞儿Faye-秀人网写真套图268" src="http://img.zngirls.com/gallery/19705/11564/cover/0.jpg" title="刘飞儿Faye-秀人网写真套图268"></a></div><div class="igalleryli_title"><a href="/g/11564/" class="caption">刘飞儿Faye-秀人网写真套图268</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/11563/"><img alt="刘飞儿Faye-[MYGIRL美媛馆]套图NO.076" src="http://img.zngirls.com/gallery/19705/11563/cover/0.jpg" title="刘飞儿Faye-[MYGIRL美媛馆]套图NO.076"></a></div><div class="igalleryli_title"><a href="/g/11563/" class="caption">刘飞儿Faye-[MYGIRL美媛馆]套图NO.076</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/11382/"><img alt="刘飞儿Faye-[XiuRen秀人VIP套图]NO.154" src="http://img.zngirls.com/gallery/19705/11382/cover/0.jpg" title="刘飞儿Faye-[XiuRen秀人VIP套图]NO.154"></a></div><div class="igalleryli_title"><a href="/g/11382/" class="caption">刘飞儿Faye-[XiuRen秀人VIP套图]NO.154</a></div></li><li class="igalleryli"><div class="igalleryli_div"><a class="igalleryli_link" href="/g/11207/"><img alt="刘飞儿Faye-微博惹火自拍照" src="http://img.zngirls.com/gallery/19705/11207/cover/0.jpg" title="刘飞儿Faye-微博惹火自拍照"></a></div><div class="igalleryli_title"><a href="/g/11207/" class="caption">刘飞儿Faye-微博惹火自拍照</a></div></li></ul></div>'''
    soup = BeautifulSoup(html)
    p = soup.find(id='photo_list').find_all(class_='caption')
    
    print type(p)
    
def visit(url, times):
    for i in range(times):
        try:
            urllib2.urlopen(url)
        except Exception, e:
            time.sleep(0.5)

def download():
    queue = Queue()
    
    path = 'D:/tmp/www.5442.com/15143'
    if not os.path.exists(path):
        os.makedirs(path)
    p = 'http://image.5442.com/2015/0213/10/{:02d}.jpg'
    count = 73
    for i in range(1, count+1):
        queue.put((path, p.format(i)))

    nthreads = 20
    for i in range(nthreads):
        t = DownloadThread(queue)
        t.start()

    queue.join()
        

if __name__ == '__main__':
##    f()
##    a = urlparse('http://www.zngirls.com/girl/19705/')
##    print a
##    download()
    url = 'http://m.mzitu.com/44836'
    urllib2.urlopen(url)
