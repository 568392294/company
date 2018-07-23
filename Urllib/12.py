#coding=utf-8
import requests

r=requests.get("http://www.baidu.com")
print(dir(r))
print(r.status_code)
print(r.url)
print("这是一个测试!")