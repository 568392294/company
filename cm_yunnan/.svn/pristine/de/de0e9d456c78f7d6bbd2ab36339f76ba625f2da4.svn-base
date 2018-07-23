# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 08:59:29 2017

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 16:10:43 2017

招投标
@author: Administrator
"""
#%%
import time
import MySQLdb
from util import mysql
from base import Tianyan
from selenium.webdriver.common.action_chains import ActionChains
class Bond(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into cmp_bond(create_time, update_time, company_name, fetch_url, \
                   publish_date, bond_name, bond_code, bond_type, rate, content, content_json) \
                   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql = "insert into cmp_bond(create_time, update_time, company_name, fetch_url) \
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
#                l = MySQLdb.escape_string(l)
                result.append(l)
            elif i == 0 or i == 1:
                result.append(int(l))
            elif i == 3:
                l = MySQLdb.escape_string(l)
                result.append(l)
            else:
                result.append(l)
        return result
    def onepage_bond_detail(self, line, k, j):
        browser = self.browser
        bond_code = line[k].find_element_by_tag_name("span").text
        #弹出页面源码部分，若弹窗不存在，重复点击至出现
        while not self.isElementExist('//table[@class="table table-striped"]'):#
            #点击详情
            line[j].find_elements_by_tag_name("span")[-1].click()
            browser.implicitly_wait(5)
        #若弹窗存在， 判断是否为所取行的详情弹窗页面   
        table_code = browser.find_elements_by_xpath('//table[@class="table table-striped"]//td')[3].text
        while bond_code != table_code:
            #不符合条件，先关闭弹窗
            browser.find_element_by_xpath('//div[@id="_modal_container"]//i[@class="tic tic-close"]').click()
            #点击详情
            line[j].find_elements_by_tag_name("span")[-1].click()
            browser.implicitly_wait(5)
            #重新获取判断条件
            table_code = browser.find_elements_by_xpath('//table[@class="table table-striped"]//td')[3].text                
        #保存源码
        option = browser.find_element_by_xpath('//div[@id="_modal_container"]')
        InnerElement = option.get_attribute('innerHTML')
        print u"获得数据 %s" % bond_code
        #关闭详情弹窗
        close = browser.find_element_by_xpath('//div[@id="_modal_container"]//i[@class="tic tic-close"]')
        ActionChains(browser).move_to_element(close).click(close).perform()
        browser.implicitly_wait(5)
        return InnerElement
                
    def onepage_data(self, company_name, company_link):
        """
        一行提交一次
        """
        browser = self.browser
        if self.isElementExist('//div[@id="_container_bond"]'):
            elements = browser.find_elements_by_xpath('//div[@id="_container_bond"]//table[@class="table  companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [curDate, curDate, company_name, company_link]
                elt = elements[i]#第 i 行
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 5:
                        data = self.onepage_bond_detail(line, 2, j)
                    else:
                        data = line[j].text
                    line_data.append(data)
                #增加字段,content_json
                originstr = line[5].find_element_by_tag_name("span").get_attribute("onclick")
                start = originstr.find('(') + 1
                end = originstr.find(')')
                content_json = originstr[start:end]
                line_data.append(content_json)
                #一行提交一次
                line_data = self.trans_encode(line_data) #转成utf-8编码
                line_data = tuple(line_data)             #转成元组数据类型
                self.insert_db(line_data, isexistdata = "yes")   
        else:#不存在著作权字段
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
win = Bond(username, password) 
win.login()   

win.turnhandle()
#%%
#==============================================================================
#                               债券信息详情
#==============================================================================
filePath = u"中国500强企业名单.xlsx" 
field = "bond"
win.fetch(filePath, field);

