#coding: utf-8
import json, urllib2, re, socket

def isdomain(host):
    '''match domain, regex is week, need to be improved'''
    domainregex = re.compile(r'([wW]{3}\.)?([a-zA-Z0-9-]+\.)+(com|org|cn|cc|net)')
    if domainregex.match(host):
        return True
    return False

def isip(host):
    arr = host.split('.')
    if len(arr) != 4:
        return False
    for i in arr:
        try:
            if not 0 <= int(i) <= 255:
                return False
        except ValueError:
            return False
    return True

def getipinfo(ip):
    '''visit taobao api'''
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip='+ip
    try:
        resp = urllib2.urlopen(url)
    except (socket.error, urllib2.URLError), e:
        return u'{"code":1,"data":"taobao api error: %s"}' % e
    return resp.read()

def parseinfo(data, encoding='utf-8'):
    '''
    {
        "code": 0,
        "data": {
            "country": "中国",
            "country_id": "CN",
            "area": "华南",
            "area_id": "800000",
            "region": "广东省",
            "region_id": "440000",
            "city": "肇庆市",
            "city_id": "441200",
            "county": "",
            "county_id": "-1",
            "isp": "移动",
            "isp_id": "100025",
            "ip": "120.234.2.210"
        }
    }
    '''
    datamap = json.loads(data, encoding=encoding)
    if datamap['code'] == 1:
        return datamap['data']
    data = datamap['data']
    r = u'%s %s%s%s %s' %(data['ip'], data['country'], data['region'],
                         data['city'], data['isp'])
    return r;

def main(host):
    if isip(host):
        return parseinfo(getipinfo(host))
    elif isdomain(host):
        try:
            ip = socket.gethostbyname(host)
        except socket.gaierror, e:
            return u'domain resolve error: %s' % e
        return parseinfo(getipinfo(ip))
    else:
        return u'argument error'

if __name__ == '__main__':
    import sys
    print main(sys.argv[1])
