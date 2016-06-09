#coding: utf8

import re, sys
import operator

def cal_toshl_bill(path):
    p = r'"\d{4}-\d{2}-\d{2}","(.+?)","(\d+\.\d{2})"'
    reg = re.compile(p)

    sum = 0
    ex_map = {}
    f = open(path)
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
            sys.stderr.write('no match: %s' % line)
    f.close()
    print sum
    ex_sorted = sorted(ex_map.items(), key=operator.itemgetter(1), reverse=True)
    for tag, cost in ex_sorted:
        print tag, cost

def cal_wx_bill(path):
    p = r'([+-]) (\d+\.\d{2})'
    reg = re.compile(p)
    income = 0
    payout = 0
    f = open(path)
    for line in f:
        m = reg.search(line)
        if m:
            if m.group(1) == '+':
                income += float(m.group(2))
            elif m.group(1) == '-':
                payout -= float(m.group(2))
            else:
                print 'unknown operator: %s' % line
    f.close()
    print 'income:%s; payout:%s; sum:%s' % (income, payout, income+payout)

if __name__ == '__main__':
    cal_toshl_bill(r'D:\tmp\url_list.txt')
