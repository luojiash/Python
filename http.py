# -*- coding utf8 -*-

import httplib, urllib

def httpreq(domain, url, data, header):
    conn = httplib.HTTPConnection(domain)
    conn.request('POST', url, data, headers)
    response = conn.getresponse()
    print response.status, response.reason
    print response.read().decode('utf8')
    conn.close()

domain = 'www.onet.com'
headers = {'Content-type': 'application/x-www-form-urlencoded',
           'cookie': 'user_name=lojashg; user_id=26; user_role=Admin'}
httpreq(domain, '/note/count', '', headers)
#httpreq(domain, '/user/login/submit', 'userName=lojashg&password=12', headers)
httpreq(domain, '/admin/user/activation', 'userId=26&active=true', headers)
