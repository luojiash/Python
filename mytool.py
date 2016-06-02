#coding: utf-8

import urllib2, re, os

filesuf = '.java'
def filefunc(f_path):
    pass

def oswalk(path):
    ''' walk from path recursively '''
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(filesuf):
                f_path = os.path.join(root, f)
                filefunc(f_path)
