#encoding: utf-8

import urllib, urllib2
import cookielib
import re
import gzip, StringIO, json
import traceback

import FileUtil

class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        print fp.read()
        return fp.read()
        
    def http_error_302(self, req, fp, code, msg, headers):
        print fp.read()
    
def ungzip(data):
    print 'decompressing...'
    #stream = StringIO.StringIO(data)
    gzipper = gzip.GzipFile(fileobj=StringIO.StringIO(data))
    return gzipper.read()
        
def getXSRF(data):
    cer = re.compile('name="_xsrf" value="(.*)"')
    m = cer.search(data)
    if m:
        return m.group(1)

def make_opener(head):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(RedirectHandler(), urllib2.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        header.append((key, value))
    opener.addheaders = header
    return opener

header = {
    'Connection': 'Keep-Alive',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Origin': 'http://www.zhihu.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With':'XMLHttpRequest'
}


opener = make_opener(header)

url = 'http://www.zhihu.com/'
f = opener.open(url)
data = f.read()
if f.headers.get('Content-Encoding') == 'gzip':
    data = ungzip(data)
_xsrf = getXSRF(data)

login_url = 'http://www.zhihu.com/login'
post_dict = {'_xsrf':_xsrf, 'email': 'bibibi@mailinator.com',
             'password': '1234abcd', 'rememberme': 'y','captcha':'asfr'}
post_data = urllib.urlencode(post_dict)
rsp = opener.open(login_url, post_data)
print rsp.getcode()
data = rsp.read()
if rsp.headers.get('Content-Encoding') == 'gzip':
    data = ungzip(data)

tdata = data.decode('unicode-escape')
FileUtil.save('f:/tmp/test.html', tdata.encode('utf8'))
print json.dumps(json.loads(data),ensure_ascii=False)
print tdata