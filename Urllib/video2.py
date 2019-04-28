import requests
import re
import time

time_start=time.time()
url='https://yt.mmstat.com/yt/vp.vdoview?platform=windows&browser=chrome&browser_version=69.0.3497.100&version=0.5.24&sid=05477e809cefce0ca34bb2eeb969e43b&videoOwnerId=1363355059&viewUserId=&videoid=825407081&Tid=0&ct=106&cs=&showid_v2=undefined&showid_v3=undefined&support_type=mp4&stg=undefined&abtest=a&Copyright=undefined&hd=1&format=2&winType=30&totalsec=344&referUrl=&url=https%3A%2F%2Fplayer.youku.com%2Fembed%2FXMzMwMTYyODMyNA%3D%3D%3Fautoplay%3Dtrue%26client_id%3D37ae6144009e277d&currentPlayTime=121&timestamp=1556184538145&topHdVideo=&fct=&number=60&show_videotype=undefined&fullflag=0&playComplete=0&unCookie=&frame=&continuationPlay=1&mtype=oth&langid=&ctype=0512&ev=1&tk=&oip=223.255.43.7&isvip=0&paystate=0&playstate=1&Type=0&pid=37ae6144009e277d&emb=&cna=XGVFFZhn3kUCAd%2F%2FKwc7e2TY&ikuflag=n&source=video&playersid=15561844161651d99t3ft62ovqMPzAp5HRU3c&danmu=0&pb=0&videotype=UGC&REQID=0b8b3e1f00000f1d5cc17d6000008834&is_pread=1&pc_i=15561674791336HX&pc_u=0&yvft=1556183389213&seid=1556183389214cR9&svstp=29&vsidc=1&vstp=29&pvid=15561844159813rlc0W&rvpvid=15561840612893RbqR8&ycid=&rycid='
r=requests.get(url,stream=True)

with open('video/test2.mp4','wb') as f:
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)

time_end=time.time()

print("下载完成！")
print("总共耗时:"+str(time_end-time_start)+'s')