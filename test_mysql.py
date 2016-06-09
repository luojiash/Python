#coding: utf-8

import urllib2, time, os, re
from urlparse import urlparse
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
from Queue import Queue


import MySQLdb

def query(cursor):
    count = cursor.execute('select * from t1')
    print '%d rows' % count
    data = cursor.fetchall()
    print data
    
if __name__ == '__main__':
    db = MySQLdb.connect('127.0.0.1', 'root', '', 'test')
    cursor = db.cursor()
    cursor.execute('insert into t1 values(3)')
    query(cursor)
    #db.commit()
    db.rollback()
    query(cursor)
    db.close()
