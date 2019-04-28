import requests
import re
import time

time_start=time.time()
url='https://pic.ibaotu.com/00/51/34/88a888piCbRB.mp4'
r=requests.get(url,stream=True)

with open('video/test.mp4','wb') as f:
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)

time_end=time.time()

print("下载完成！")
print("总共耗时:"+str(time_end-time_start)+'s')
