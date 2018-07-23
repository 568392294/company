#coding=utf-8

import urllib.request

file=urllib.request.urlopen("http://www.baidu.com")
data=file.read()
fhandle=open("D:/python/Urllib/1.html","wb")
fhandle.write(data)
fhandle.close()
dataline=file.readline()
print(data)
#print(dataline)