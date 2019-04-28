#coding=utf-8

#urllib模块提供了读取Web页面数据的接口
import urllib.request
#re模块主要包含了正则表达式
import re
#定义一个getHtml()函数
# def getHtml(url):
#     page = urllib.urlopen(url)  #urllib.urlopen()方法用于打开一个URL地址
#     html = page.read() #read()方法用于读取URL上的数据
#     return html

def getImg(html):
    # reg = r'src="(.+?\.jpg)" pic_ext'    #正则表达式，得到图片地址
    # imgre = re.compile(reg)     #re.compile() 可以把正则表达式编译成一个正则表达式对象.
    # imglist = re.findall(imgre,html)      #re.findall() 方法读取html 中包含 imgre（正则表达式）的    数据
    # #把筛选的图片地址通过for循环遍历并保存到本地
    # #核心是urllib.urlretrieve()方法,直接将远程数据下载到本地，图片通过x依次递增命名
    # x = 0

    for i in range(175):
        imgurl=html+str(i+1)+".gif"
        print(imgurl)
        urllib.request.urlretrieve(imgurl,'D:\pdf\%s.jpg' % str(i+100))

html = getImg("http://www.3mbang.com/FileRoot0/2017-1/12/76dbbf18-3056-474e-9dc0-0ac1c55e784b/76dbbf18-3056-474e-9dc0-0ac1c55e784b")