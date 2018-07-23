import urllib.request
import urllib.parse

url="https://mail.qq.com/"
postdata=urllib.parse.urlencode({
	"u":"568392294@qq.com",
	"p":"210878492"
	}).encode('utf-8')
req=urllib.request.Request(url,postdata)
req.add_header('Usr-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppliWebKit/537.36 (KHTML,like Gecko) Chrome/38.0.2125.122 safari/537.36 SE 2.X MetaSr 1.0')
data=urllib.request.urlopen(req).read()
fhandle=open("D:/python/Urllib/7.html","wb")
fhandle.write(data)
fhandle.close()
