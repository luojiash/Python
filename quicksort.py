#coding:utf-8
import random
import datetime

def quicksort(data, low, high):
    if low >= high:
        return
    
    key = data[high-1]
    i = low

    for j in range(low, high - 1):
        if data[j] <= key:
            data[i], data[j] = data[j], data[i]
            i += 1
    data[i], data[high - 1] = key, data[i]

    quicksort(data, low, i)
    quicksort(data, i + 1, high)

data = [random.randint(0, 65536) for i in range(3000)]
t1 = datetime.datetime.now()
quicksort(data, 0, len(data))
t2 = datetime.datetime.now()
print(data)
print(t2 - t1)

            
        
