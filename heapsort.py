# -*- coding: utf-8 -*-

import random

def heapsort(data):
    n = len(data)
    for i in range(n // 2 - 1, -1, -1):
        sink(data, i, n)
    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        sink(data, 0, i)

def sink(data, i, n):
    while 2 * i + 1 < n:
        j = 2 * i + 1
        if j + 1 < n and data[j] < data[j + 1]: j = j + 1
        if data[i] >= data[j]: break
        data[i], data[j] = data[j], data[i]
        i = j


if __name__ == '__main__':
    data = [random.randint(0, 65536) for i in range(1000)]
    heapsort(data)
    print(data)
