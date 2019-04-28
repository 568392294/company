import urllib.request
import os
import re

def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    response = urllib.request.urlopen(url)
    html = response.read()
    return html
    pass

def get_page(url):
    html=url_open(url).decode('utf-8')

    page_num=re.search(r'<span class="current-comment-page">\[(.*?)\]</span>',html)

    if page_num:
        return int(page_num.group(1))
    else:
        return None
    pass

def find_imgs(url):
    html=url_open(url).decode('utf-8')
    img_addrs=re.findall(r'<a href="(//wx\d.sinaimg.cn/.+?)" target="_blank" class="view_img_link">',html)
    return img_addrs

    pass

def save_imgs(folder,img_addrs):
    for each in img_addrs:
        finame=each.split('/')[-1]
        with open(finame,'wb') as f:
            img=url_open("http:"+each)
            f.write(img)
            print("http:"+each)
    pass

def download_mm(folder="OOXX",pages=10):
    if os.path.exists(folder)==False:
        os.mkdir(folder)
    os.chdir(folder)

    url='http://jandan.net/ooxx'
    page_num=get_page(url)

    for i in range(pages):
        page_num-=1
        if page_num>0:
            page_url='http://jandan.net/ooxx/page-'+str(page_num)+'#comments'
            img_addrs=find_imgs(page_url)
            save_imgs(folder,img_addrs)

if __name__=="__main__":
    download_mm()