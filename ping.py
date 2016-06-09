#coding:utf8
import os

def pinger(ip):
    ping = "ping -n 1 "+ip
    data = os.system(ping)
    if data == 0:
        print ip, "is connected"
    else:
        print ip, "down"

pinger('127.0.0.1')
