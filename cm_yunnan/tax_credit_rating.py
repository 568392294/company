# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 16:32:01 2017

@author: Administrator
"""

#%%
import time
from selenium.webdriver.common.action_chains import ActionChains
from util import mysql
from base import Tianyan
import MySQLdb


class TaxCR(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into cmp_tax_credit_rating(create_time, update_time, company_name, fetch_url, \
                   year, tax_rating, tax_type, taxpayer_id, evaluation_unit, unique_key)  \
                   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql = "insert into cmp_tax_credit_rating(create_time, update_time, company_name, fetch_url) \
                   values(%s, %s, %s, %s)"
        # 执行sql语句
        result = mysql.execute(sql, line)
        print result
    def trans_encode(self,alist):
        """
        将列表中的各个元素转换成utf-8编码
        """
        result = []
        for i in range(len(alist)):
            l = alist[i]
            if type(l) == unicode:
                l = l.encode("utf-8")
                result.append(l)
            elif i == 0 or i == 1:
                result.append(int(l))
            elif i == 3:
                l = MySQLdb.escape_string(l)
                result.append(l)
            else:
                result.append(l)
        return result
    
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_taxcredit"]'):
            elements = browser.find_elements_by_xpath('//div[@id="_container_taxcredit"]//table[@class="table companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [curDate, curDate, company_name, company_link]
                elt = elements[i]#第 i 行
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    data = line[j].text
                    line_data.append(data)
                #生成加密键值
                comb = line_data[4] + line_data[5] + line_data[6] + line_data[7]
                unique_key = self.md5(comb.encode("utf-8"))
                line_data.append(unique_key)
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
win = TaxCR(username, password) 
win.login()   

win.turnhandle()

#%%
#==============================================================================
#                               税务评级详情
#==============================================================================
filePath = u"1000家企业.xlsx" 
field = "taxcredit"
win.fetch(filePath, field);

