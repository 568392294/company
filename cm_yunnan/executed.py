# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:56:28 2017

@author: Administrator
"""


#%%
import time
from selenium.webdriver.common.action_chains import ActionChains
from util import mysql
from base import Tianyan



class Zhixing(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into cmp_executed(create_time, update_time, company_name, fetch_url, \
                   register_date, enforcement_object, case_no, executive_court)  \
                   values(%s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql = "insert into cmp_executed(create_time, update_time, company_name, fetch_url) \
                   values(%s, %s, %s, %s)"
        # 执行sql语句
        result = mysql.execute(sql, line)
        print result
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_zhixing"]'):
            elements = browser.find_elements_by_xpath('//div[@id="_container_zhixing"]//table[@class="table companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [curDate, curDate, company_name, company_link]
                elt = elements[i]#第 i 行
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    data = line[j].text
                    line_data.append(data)
                #一行提交一次
                line_data = self.trans_encode(line_data) #转成utf-8编码
                line_data = tuple(line_data)             #转成元组数据类型
                self.insert_db(line_data, isexistdata = "yes")   
        else:#不存在失信人字段
            curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
            line_data = [curDate, curDate, company_name, company_link]
            line_data = self.trans_encode(line_data) #转成utf-8编码
            line_data = tuple(line_data)             #转成元组数据类型
            self.insert_db(line_data, isexistdata = "no")   
#        return line_data

            
#%%                              
#==============================================================================
#                               登录
#==============================================================================
username = "18064063503"   #第一个参数为用户名
password = "wzswjmm123"   #第二个参数为密码
win = Zhixing(username, password) 
win.login()   

win.turnhandle()

#%%
#==============================================================================
#                               被执行人详情
#==============================================================================
filePath = u"中国500强企业名单.xlsx" 
field = "zhixing"
win.fetch(filePath, field);
