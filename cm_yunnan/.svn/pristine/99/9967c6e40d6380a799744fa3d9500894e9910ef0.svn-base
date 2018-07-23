# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 13:32:04 2017

商标

@author: Administrator
"""
#%%
import time
from util import mysql
from base import Tianyan

class TradeMark(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into cmp_trademark(create_time, update_time, company_name, fetch_url, \
                   apply_date, logo, trademark, register_number, \
                   classification, status)  \
                   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql = "insert into cmp_trademark(create_time, update_time, company_name, fetch_url) \
                   values(%s, %s, %s, %s)"
        # 执行sql语句
        result = mysql.execute(sql, line)
        print result
        
#    def trans_encode_trademark(self,alist):
#        """
#        将列表中的各个元素转换成utf-8编码
#        """
#        result = []
#        for i in range(len(alist)):
#            l = alist[i]
#            if type(l) == unicode:
#                l = l.encode("utf-8")
##                l = MySQLdb.escape_string(l)
#                result.append(l)
#            elif i == 0 or i == 1:
#                result.append(int(l))
#            elif i == 3:
#                l = MySQLdb.escape_string(l)
#                result.append(l)
#            else:
#                result.append(l)
#        return result
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_tmInfo"]'):
            elements = browser.find_elements_by_xpath('//div[@id="_container_tmInfo"]//table[@class="table  companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [curDate, curDate, company_name, company_link]
                elt = elements[i]
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 1: 
                        data = line[j].find_element_by_tag_name("img").get_attribute("src")
                        data = data.encode("utf-8")
                    else:
                        data = line[j].text
                    line_data.append(data)
                #一行提交一次
                line_data = self.trans_encode(line_data) #转成utf-8编码
                line_data = tuple(line_data)             #转成元组数据类型
                self.insert_db(line_data, isexistdata = "yes")  
        else: #不存在商标字段
            curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
            line_data = [curDate, curDate, company_name, company_link]
            line_data = self.trans_encode(line_data) #转成utf-8编码
            line_data = tuple(line_data)             #转成元组数据类型
            self.insert_db(line_data, isexistdata = "no")   
                
            
#%%                              
#==============================================================================
#                               登录
#==============================================================================
username = "18064063503"   #第一个参数为用户名
password = "wzswjmm123"   #第二个参数为密码
win = TradeMark(username, password) 
win.login()   

win.turnhandle()
#%%
#==============================================================================
#                               商标详情
#==============================================================================
filePath = u"1000家企业.xlsx" 
field = "tmInfo"
win.fetch(filePath, field);
