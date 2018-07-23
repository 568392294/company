# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:29:13 2017

失信被执行人
@author: Administrator
"""


#%%
import time
from selenium.webdriver.common.action_chains import ActionChains
from util import mysql
from base import Tianyan



class Dishonest(Tianyan):
    
    def insert_db(self, line, isexistdata="yes"):
        # SQL 插入语句
        if isexistdata == "yes":
            sql = "insert into cmp_dishonest(create_time, update_time, company_name, fetch_url, \
                   register_date, case_no, courtname, performance, \
                   gist_id, content, content_json)  \
                   values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            sql = "insert into cmp_dishonest(create_time, update_time, company_name, fetch_url) \
                   values(%s, %s, %s, %s)"
        # 执行sql语句
        result = mysql.execute(sql, line)
        print result
    def onepage_dishonest_detail(self, line, k, j):
        browser = self.browser
        softw_name = line[k].find_element_by_tag_name("span").text
        #弹出页面源码部分，若弹窗不存在，重复点击至出现
        while not self.isElementExist('//div[@class="modal-body"]/table[@class="table companyInfo-table"]'):#
            #点击详情
            line[j].find_elements_by_tag_name("span")[-1].click()
            browser.implicitly_wait(5)
        #若弹窗存在， 判断是否为所取行的详情弹窗页面   
        table_name = browser.find_elements_by_xpath('//div[@class="modal-body"]/table[@class="table companyInfo-table"]//td')[9].text
        while table_name != softw_name:
            #不符合条件，先关闭弹窗
            browser.find_element_by_xpath('//div[@id="_modal_container"]//i[@class="tic tic-close"]').click()
            #点击详情
            line[j].find_elements_by_tag_name("span")[-1].click()
            browser.implicitly_wait(5)
            #重新获取判断条件
            table_name = browser.find_elements_by_xpath('//div[@class="modal-body"]/table[@class="table companyInfo-table"]//td')[9].text
        #保存源码
        option = browser.find_element_by_xpath('//div[@id="_modal_container"]')
        InnerElement = option.get_attribute('innerHTML')
        print u"获得数据 %s" % softw_name
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
        if self.isElementExist('//div[@tyc-event-ch="CompangyDetail.shixinren"]'):
            elements = browser.find_elements_by_xpath('//div[@tyc-event-ch="CompangyDetail.shixinren"]//table[@class="table  companyInfo-table"]/tbody/tr')
            for i in range(len(elements)):
                #第 i 行
                curDate = time.strftime("%Y%m%d%H%M%S")#当前日期
                line_data = [curDate, curDate, company_name, company_link]
                elt = elements[i]#第 i 行
                line = elt.find_elements_by_tag_name("td")
                for j in range(len(line)):
                    if j == 5:
                        data = self.onepage_dishonest_detail(line, 1, j)
                    else:
                        data = line[j].text
                    line_data.append(data)
                #增加字段,content_json
                originstr = line[5].find_element_by_tag_name("span").get_attribute("onclick")
                start = originstr.find('(') + 1
                end = len(originstr) - 1
                content_json = originstr[start:end]
                line_data.append(content_json)
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
username = "15623247485"   #第一个参数为用户名
password = "123456abc"   #第二个参数为密码
win = Dishonest(username, password) 
win.login()   

win.turnhandle()

#%%
#==============================================================================
#                               失信人详情
#==============================================================================
filePath = u"1000家企业.xlsx" 
field = "dishonest"
win.fetch(filePath, field);
