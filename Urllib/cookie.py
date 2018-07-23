import urllib.request
import urllib.parse
import http.cookiejar

url="http://bbs.chinaunix.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=L768q"
postdata=urllib.parse.urlencode({
    "username":"weisuen",
    "password":"aA123456"
}).encode("utf-8")

req=urllib.request.Request(url,postdata)
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0')
cjar=http.cookiejar.CookieJar()
opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))

urllib.request.install_opener(opener)
file=opener.open(req)
data=file.read()
file=open("D:/python/html/3.html","wb")
file.write(data)
file.close()

url2="http://bbs.chinaunix.net"
data2=urllib.request.urlopen(url2).read()
fhandle=open("D:/python/html/4.html","wb")
fhandle.write(data2)
fhandle.close()