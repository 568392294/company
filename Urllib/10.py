import urllib.request
from urllib import error
try:
    urllib.request.urlopen("http://blohg.csdn.net")
except error.HTTPError as e:
    print(e.code)
    print(e.reason)
except error.URLError as e:
    print(e.reason)

