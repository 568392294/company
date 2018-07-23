import re
import urllib.request

def craw(url,page):
	html1=urllib.request.urlopen(url).read()
	html1=str(html1)
	pat1='<div class="MeinvTuPianBox">.+?<div class="hr10">'
	result1=re.compile(pat1).findall(html1)
	result1=result1[0]
	print(result1)
	pat2='<img src="http//(.+?\.jpg)"'
	imagelist=re.compile(pat2).findall(result1)
	#print(imagelist)
	x=1
	for imageurl in imagelist:
		print(imageurl)
		imagename="D:/python/Urllib/img/"+str(page)+str(x)+".jpg"
		imageurl="https://"+imageurl
		try:
			urllib.request.urlretrieve(imageurl,filename=imagename)
		except urllib.error.URLError as e:
			if hasattr(a,"code"):
				x+=1
			if hasattr(a,"reason"):
				x+=1
		x+=1
for i in range(1,2):
	url="http://www.27270.com/ent/meinvtupian/list_11_"+str(i)+".html"
#url="https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&cid2=653&cid3=655&page=1&s=1&click=0"
	craw(url,i)