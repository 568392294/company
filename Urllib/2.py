import urllib.request

url="http://blog.csdn.net/weiwei_pig/article/details/51178226"
file=urllib.request.urlopen(url)
data=file.read()
print(data)