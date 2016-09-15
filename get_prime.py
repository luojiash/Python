#coding: utf8

def getPrime(max):
    ''' 获得小于max 的所有质数 '''
    # 标记数组，True 表示是质数
    aList = [True for x in range(0, max)]
    prime = []
    for x in range(2, max):
        if aList[x]:
            prime.append(x)
            # 标记质数的倍数
            for y in range(2, (max/x)+1):
                if x * y < max:
                    aList[x * y] = False
    return prime

print getPrime(150)
