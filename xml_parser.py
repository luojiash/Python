#coding: utf-8
from xml.dom import minidom
import StringIO

content='''<?xml version="1.0"?>
<SabreCommandLLSRS>
<Response>
    <![CDATA[L]]>
</Response>
</SabreCommandLLSRS>'''

def ex1():
    fobj = StringIO.StringIO(content)
    doc = minidom.parse(fobj)
    fobj.close()
    # Response元素有3个子节点，包括前后的换行/空白符，中间的CDATA节点
    resp = doc.getElementsByTagName('Response')[0]
    print resp.firstChild
    print resp.childNodes[1].data # L
    print resp.lastChild

if __name__=='__main__':
    ex1()
