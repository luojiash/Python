#coding: utf8

import re
import operator

def f1():
    p = r'"\d{4}-\d{2}-\d{2}","(.+?)","(\d+\.\d{2})"'
    reg = re.compile(p)

    sum = 0
    ex_map = {}
    f = open('h:/baiduyundownload/data.txt')
    for line in f:
        m = reg.match(line)
        if m:
            tags = m.group(1).decode('utf8').split(', ')
            cost = float(m.group(2))
            sum += cost
            for tag in tags:
                if ex_map.has_key(tag):
                    ex_map[tag] += cost
                else:
                    ex_map[tag] = cost
            #print m.group(1).decode('utf8'), m.group(2)
        else:
            print 'no match: %s' % line
    f.close()
    print sum
    ex_sorted = sorted(ex_map.items(), key=operator.itemgetter(1), reverse=True)
    for tag, cost in ex_sorted:
        print tag, cost

def f2():
    p = r'([+-]) (\d+\.\d{2})'
    reg = re.compile(p)
    sum = 0
    f = open('h:/baiduyundownload/data.txt')
    for line in f:
        m = reg.search(line)
        if m:
            if m.group(1) == '+':
                sum += float(m.group(2))
            elif m.group(1) == '-':
                sum -= float(m.group(2))
            else:
                print 'unknown operator: %s' % line
    f.close()
    print sum

f2()
