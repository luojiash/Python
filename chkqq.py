#encoding: utf-8
import urllib2,time
from Tkinter import *
import tkMessageBox

def chk_qq(qqnum):
    try:
        resp = urllib2.urlopen('http://wpa.paipai.com/pa?p=1:'+qqnum+':17')
    except urllib2.URLError, e:
        print e
        return
    length = resp.headers.get('content-length')
    if length == '2205':
        return 'offline'
    return 'online'

if __name__ == '__main__':
    qqnum = '123456789'
    while True:
        r = chk_qq(qqnum)
        if r == 'offline':
            print r
            tkMessageBox.showinfo(message=r)
            break;
        time.sleep(45)
