#coding: utf-8

import Image
import os

def filter_img(source, target):
    count = 0
    i = 0
    target_i = os.path.join(target, str(i))
    if not os.path.exists(target_i):
        os.makedirs(target_i)
    
    for root, dirs, files in os.walk(source):
        if count > 25:
            count = 0
            i += 1
            target_i = os.path.join(target, str(i))
            if not os.path.exists(target_i):
                os.makedirs(target_i)
            
        for f in files:
            fsrc = os.path.join(root, f)
            try:
                img = Image.open(fsrc)
                size = img.size
                if size[1] > size[0]:
                    ftar = os.path.join(target_i, f)
                    if os.path.isfile(ftar):
                        ftar.replace('.', '_1.')
                    if os.path.isfile(ftar):
                        print '%s->%s' % (fsrc, ftar)
                    else:
                        img.save(ftar)
                        count += 1
            except Exception, e:
                print "%s: %s" % (e, f)
            
        
if __name__ == '__main__':
    filter_img('d:/tmp/b', 'd:/tmp/abc')
