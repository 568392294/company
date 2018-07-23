import urllib.request
import urllib.error

try:
	urllib.request.urlopen("http://www.1111.com/zlts/0-0-0-0-0-0_0-0-1.shtml")
except urllib.error.URLError as e:
	print(e.code)
	print(e.reason)