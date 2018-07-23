import urllib.request
import re

def getlink(url):
    header=('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
    opener=urllib.request.build_opener()
    opener.addheaders=[header]

    urllib.request.install_opener(opener)
    file=urllib.request.urlopen(url)
    data=str(file.read())

    #pat='(https?://[^\s)";]+\.(\w|/)*)'
    pat='(https?://[^\s)";]+\.(\w|/)*)'
    link=re.compile(pat).findall(data)

    link=list(set(link))
    return link

url="http://blog.csdn.net/"
linklist=getlink(url)
for link in linklist:
    print(link[0])