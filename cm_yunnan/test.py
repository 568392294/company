# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:10:43 2017

招投标
@author: Administrator
"""
#%%
import re
import uuid
#import cx_Oracle
from util import oracle

sql = "select count(0) from \"cmp_lawsuit\""
#conn = cx_Oracle.connect('zwy_test','zwy_test123','172.16.50.131:1521/orcl')  
#cursor = conn.cursor()  
#cursor.execute(sql)  
#data = cursor.fetchall()  
#print(data)  

result = oracle.executeQuery(sql, None)
print result


#%% 



uid = str(uuid.uuid1())
print uid.replace('-','')

#获取分页总数
content = u"共10页"
p = re.compile(ur"共(\d+)页")
m = p.search(content)
if m:
    pageCount = int(m.group(1))
    print pageCount