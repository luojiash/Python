# -*- coding: utf-8 -*-

import os

def listdir(path):
    ''' list the names of the entries in a directory '''
    for fname in os.listdir(path):
        fullpath = os.path.join(path, fname)
        if os.path.isdir(fullpath):
            print fullpath, os.path.basename(fullpath)
        else:
            size = os.path.getsize(fullpath)
            print fullpath, size

def oswalk(path):
    ''' walk from path recursively '''
    for root, dirs, files in os.walk(path):
        print root
        print dirs
        print files

def save(path, data):
    file = open(path, 'wb')
    file.write(data)
    file.close()

listdir(u'F:\software')
# oswalk(u'F:\software')