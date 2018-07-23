import re

#pattern="\w\dpython\w"
pattern="[a-zA-Z]+://[^\s]*[.com|.cn]"
string="<div><span><a href='http://www.baidu.com'></a></span><span>sjjjes@iqianyue.com</span></div>"
result1=re.search(pattern,string)
print(result1)