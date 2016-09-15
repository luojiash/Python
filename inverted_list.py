#coding:utf-8

''' 倒排索引
'''
def invert(file):
    result = {}
    for line in file:
        left, right = line.split()
        if right in result:
            result[right].append(left)
        else:
            result[right] = [left]
    return result

file = open('inverted_list.txt', 'r')
result = invert(file)
for (right, lefts) in result.items():
    print(len(lefts), right, lefts)
