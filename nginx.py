#coding: utf-8

from Tkinter import *
import os, subprocess

def findTask():
    cmd = 'tasklist | findstr nginx.exe'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    var.set(p.stdout.read())

def start():
    cmd = 'start nginx.exe'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    #var.set(p.stdout.read())
    
def stop():
    cmd = 'nginx.exe -s stop'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    var.set(p.stdout.read())
    
def reload():
    cmd = 'nginx.exe -s reload'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    var.set(p.stdout.read())
    
top = Tk()
#top.geometry('650x150')

var = StringVar()
res = Message(top, textvariable=var, relief = 'raised', width=80)
res.pack(fill=X, expand=1)

refresh = Button(top, text='refresh', command=findTask)
refresh.pack(fill=X, expand=1)

s = Button(top, text='start', command=start)
s.pack(fill=X, expand=1)
st = Button(top, text='stop', command=stop)
st.pack(fill=X, expand=1)
r = Button(top, text='reload', command=reload)
r.pack(fill=X, expand=1)

quit = Button(top, text='EXIT', command=top.destroy)
quit.pack(fill=X, expand=1)

os.chdir('D:/nginx-1.4.3')
mainloop()
